def get_session_and_account():
    """
    Create and return a Tastytrade session and the first available account.
    Raises ValueError if there is a problem.
    """
    import keyring
    from tastytrade import Session, Account

    username = keyring.get_password("tastytrade", "username")
    password = keyring.get_password("tastytrade", "password")

    if not username or not password:
        raise ValueError("Missing Tastytrade credentials in keyring. Use keyring.set_password() to set them.")

    session = Session(username, password)
    if not session:
        raise ValueError("Failed to create Tastytrade session.")

    accounts = Account.get_accounts(session)
    if not accounts:
        raise ValueError("No valid accounts found.")

    return session, accounts[0]
