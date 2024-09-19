import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .constants import MAIL_PROVIDER, GMAIL_TOKEN_PATH, GMAIL_SCOPES, GMAIL_CREDENTIALS_PATH
from .services.gmail import GmailService


def get_mail_service():
    if MAIL_PROVIDER == 'gmail':
        return GmailService()
    else:
        raise ValueError(f"Mail provider {MAIL_PROVIDER} is not supported.")


def create_gmail_token():
    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, GMAIL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, GMAIL_SCOPES)
            creds = flow.run_local_server(port=62884)

        with open(GMAIL_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
