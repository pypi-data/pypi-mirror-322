from msal import PublicClientApplication

def authenticate():
    client_id = "<YOUR_CLIENT_ID>"
    authority = "https://login.microsoftonline.com/<TENANT_ID>"
    scopes = ["User.Read"]

    app = PublicClientApplication(client_id=client_id, authority=authority)
    result = None

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])

    if not result:
        result = app.acquire_token_interactive(scopes)

    return result["access_token"] if result else None
