from src.constants import POLL_TIMEOUT
from src.email_daemon import EmailDaemon
from src.utils import create_gmail_token

if __name__ == "__main__":
    create_gmail_token()
    daemon = EmailDaemon(poll_interval=POLL_TIMEOUT)
    daemon.run()
