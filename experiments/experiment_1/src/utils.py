from experiments.experiment_1.src.constants import MAIL_PROVIDER


def get_mail_service():
    if MAIL_PROVIDER == 'gmail':
        from experiments.experiment_1.src.services.gmail import GmailService
        return GmailService()
    else:
        raise ValueError(f"Mail provider {MAIL_PROVIDER} is not supported.")