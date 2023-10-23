import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials 
from google.auth.transport.requests import Request

import sys

SCOPE = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/gmail.readonly"]

def request_creds():
    creds = None
    if os.path.exists('client_secret.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=SCOPE)
        creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file('token.json', SCOPE)

    else:
        print("cred not present")
        sys.exit(1)


def  get_creds():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPE)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    return request_creds()
    