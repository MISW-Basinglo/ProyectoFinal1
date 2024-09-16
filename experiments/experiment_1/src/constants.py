import os

PUBSUB_PROJECT_ID = os.getenv('PUBSUB_PROJECT_ID', "my-project")
PUBSUB_TOPIC = os.getenv('PUBSUB_TOPIC', "emails")
MAIL_PROVIDER = os.getenv('MAIL_PROVIDER', "gmail")
GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', "experiments/experiment_1/mail_client.json")
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
POLL_TIMEOUT = os.getenv("POLL_TIMEOUT", 5)
