import keyring
from getpass import getpass
from .auth import get_session_and_account

def setup_tastytrade_auth():
    """Interactive command-line setup for Tastytrade credentials."""
    print("Setting up Tastytrade credentials")
    print("=================================")

    username = input("Enter your Tastytrade username: ")
    password = getpass("Enter your Tastytrade password: ")  # getpass hides the password while typing

    try:
        # Store credentials
        keyring.set_password("tastytrade", "username", username)
        keyring.set_password("tastytrade", "password", password)

        # Verify credentials work
        session, account = get_session_and_account()
        print("\nCredentials verified successfully!")
        print(f"Connected to account: {account.account_number}")

    except Exception as e:
        print(f"\nError setting up credentials: {str(e)}")
        # Clean up on failure
        keyring.delete_password("tastytrade", "username")
        keyring.delete_password("tastytrade", "password")
        return False

    return True

if __name__ == "__main__":
    setup_tastytrade_auth()