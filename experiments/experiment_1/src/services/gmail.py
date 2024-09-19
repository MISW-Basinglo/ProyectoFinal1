from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.constants import GMAIL_TOKEN_PATH, GMAIL_SCOPES
from src.services.mail_service import MailService
import logging


class GmailService(MailService):
    def __init__(self):
        self.creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, GMAIL_SCOPES)
        self.service = build('gmail', 'v1', credentials=self.creds)

    def fetch_unread_emails(self):
        try:
            result = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = result.get('messages', [])

            email_data = []
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                email_data.append({
                    "id": msg['id'],
                    "subject": self.get_header(msg['payload']['headers'], 'Subject'),
                    "from": self.get_header(msg['payload']['headers'], 'From'),
                    "body": msg['snippet']
                })
            return email_data
        except Exception as e:
            logging.info(f"Error fetching unread emails: {e}")
            return []

    def mark_as_read(self, message_id):
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            logging.error(f"Error marking email as read: {e}")

    @staticmethod
    def get_header(headers, name):
        for header in headers:
            if header['name'] == name:
                return header['value']
        return None
