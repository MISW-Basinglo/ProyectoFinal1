from experiments.experiment_1.src.constants import POLL_TIMEOUT
from experiments.experiment_1.src.email_daemon import EmailDaemon
from experiments.experiment_1.src.utils import create_gmail_token

if __name__ == "__main__":
    create_gmail_token()
    daemon = EmailDaemon(poll_interval=POLL_TIMEOUT)
    daemon.run()
