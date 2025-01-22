import asyncio
import json
import logging
from typing import Literal
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from src.tastytrade_api.functions import get_bid_ask_price, _place_order

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parents[2] # this file is in src/core
DATA_DIR = PROJECT_ROOT / "data"

class OrderManager:
    """
    Encapsulates the order queue and related logic.
    """

    def __init__(self, queue_file: Path = DATA_DIR / "order_queue.json"):
        # Create data directory if it doesn't exist
        DATA_DIR.mkdir(exist_ok=True)

        self.queue_file = queue_file
        # Holds all queued tasks by group: {group_number: [ {order_item_dict}, ... ], ...}
        self.task_queue: dict[int, list[dict]] = {}

    def load_queue_from_file(self) -> None:
        """
        Loads tasks from self.queue_file into self.task_queue (in-memory).
        If the file is missing or empty, this is a no-op.
        """
        if not self.queue_file.is_file():
            return

        try:
            logger.info(f"Looking for: {self.queue_file.resolve()}")
            with open(self.queue_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert keys back from string into int
            self.task_queue = {int(k): v for k, v in data.items()}
            logger.info("Loaded %d groups from %s", len(self.task_queue), self.queue_file)
        except Exception as e:
            logger.error("Error loading %s: %s", self.queue_file, str(e))

    def save_queue_to_file(self) -> None:
        """
        Saves the current self.task_queue to disk in JSON format.
        """
        serializable = {str(k): v for k, v in self.task_queue.items()}
        try:
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2)
            logger.info("Successfully saved queue to %s", self.queue_file)
        except Exception as e:
            logger.error("Error saving %s: %s", self.queue_file, str(e))

    async def queue_order(
        self,
        symbol: str,
        quantity: int,
        action: Literal['BUY_TO_OPEN', 'SELL_TO_CLOSE'],
        execution_group: int = 1,
        dry_run: bool = True
    ) -> str:
        """
        Queues an order for execution, storing symbol, quantity, action, group, and dry_run.
        The actual bid/ask retrieval and limit price calculation now occur at runtime
        within execute_queued_tasks().
        """
        # Load current datastore
        self.load_queue_from_file()

        if execution_group not in self.task_queue:
            self.task_queue[execution_group] = []

        # We no longer pre-calculate price here:
        self.task_queue[execution_group].append({
            "symbol": symbol,
            "quantity": quantity,
            "action": action,
            "dry_run": dry_run
        })

        # Save updated queue to disk
        self.save_queue_to_file()

        return (
            f"Order queued: symbol={symbol}, qty={quantity}, "
            f"action={action}, (execution_group={execution_group})."
        )

    async def execute_queued_tasks(self, session, account):
        """
        Executes all queued tasks (in ascending order of their execution_group).
        Within the same group, tasks run in parallel (async).

        This method also fetches the bid/ask and calculates the limit price at runtime.
        After all tasks are completed, the queue is cleared from memory and on disk.
        """
        # Reload the queue from file to ensure freshness
        self.load_queue_from_file()

        # Sort groups lowest to highest
        sorted_groups = sorted(self.task_queue.keys())
        for group in sorted_groups:
            tasks = self.task_queue[group]
            if not tasks:
                continue

            logger.info("Executing group=%s with %d tasks...", group, len(tasks))
            coros = []
            for idx, t in enumerate(tasks):
                # Fetch current bid/ask
                bid, ask = await get_bid_ask_price(session, t["symbol"])
                logger.info("Fetched bid=%s, ask=%s for symbol=%s", bid, ask, t["symbol"])

                # Compute mid price, ensure two decimal places
                raw_mid = (bid + ask) / 2
                limit_price = Decimal(raw_mid).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                # Place order using the runtime price
                coro = _place_order(
                    session,
                    account,
                    t["symbol"],
                    t["quantity"],
                    float(limit_price),
                    t["action"],
                    dry_run=t["dry_run"],
                )
                coros.append(coro)

            results = await asyncio.gather(*coros, return_exceptions=True)
            for idx, res in enumerate(results):
                if isinstance(res, Exception):
                    logger.error(
                        "Task %d in group %s raised an exception: %s",
                        idx, group, str(res)
                    )
                else:
                    logger.info(
                        "Task %d in group %s completed: %s",
                        idx, group, res
                    )

        # Clear tasks from in-memory queue and file
        self.task_queue.clear()
        self.save_queue_to_file()
        logger.info("All queued tasks have been executed.")

    def cancel_queued_orders(self, execution_group: int | None = None, symbol: str | None = None) -> str:
        """
        Cancels queued orders based on provided filters.

        Args:
            execution_group: If provided, only cancels orders in this group.
                            If None, considers orders in all groups.
            symbol: If provided, only cancels orders for this symbol.
                    If None, considers all symbols.

        Returns:
            A message describing what was cancelled.
        """
        # Load current queue state
        self.load_queue_from_file()

        cancelled_count = 0
        if execution_group is not None:
            # Cancel orders in specific group
            if execution_group in self.task_queue:
                if symbol is not None:
                    # Remove only orders matching the symbol
                    original_len = len(self.task_queue[execution_group])
                    self.task_queue[execution_group] = [
                        order for order in self.task_queue[execution_group]
                        if order["symbol"] != symbol
                    ]
                    cancelled_count = original_len - len(self.task_queue[execution_group])
                else:
                    # Remove all orders in the group
                    cancelled_count = len(self.task_queue[execution_group])
                    del self.task_queue[execution_group]
        else:
            # Process all groups
            groups_to_delete = []
            for group, orders in self.task_queue.items():
                if symbol is not None:
                    # Remove only orders matching the symbol
                    original_len = len(orders)
                    self.task_queue[group] = [
                        order for order in orders
                        if order["symbol"] != symbol
                    ]
                    cancelled_count += original_len - len(self.task_queue[group])
                    if not self.task_queue[group]:
                        groups_to_delete.append(group)
                else:
                    # Remove all orders
                    cancelled_count += len(orders)
                    groups_to_delete.append(group)

            # Clean up empty groups
            for group in groups_to_delete:
                del self.task_queue[group]

        # Save updated queue
        self.save_queue_to_file()

        return f"Cancelled {cancelled_count} order{'s' if cancelled_count != 1 else ''}"