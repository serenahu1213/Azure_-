#取得token，方便日後減少pin使用
#若 第一次使用請執行此檔，取得 access_token, refresh_token
#若 token 失效 也請再次執行此檔案

from imgurpython import ImgurClient
from config import client_id, client_secret


def get_input(string):
    return input(string)


def authenticate():
    # Get client ID and secret from config.py

    client = ImgurClient(client_id, client_secret)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    # Read in the pin, handle Python 2 or 3 here.
    pin = get_input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))

    return client


# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
    authenticate()