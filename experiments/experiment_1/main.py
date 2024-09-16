from experiments.experiment_1.src.constants import POLL_TIMEOUT
from experiments.experiment_1.src.email_daemon import EmailDaemon

if __name__ == "__main__":
    daemon = EmailDaemon(poll_interval=POLL_TIMEOUT)
    daemon.run()
