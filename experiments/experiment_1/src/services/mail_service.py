from abc import ABC, abstractmethod


class MailService(ABC):

    @abstractmethod
    def fetch_unread_emails(self):
        """Obtiene los correos no leídos del servicio de email."""
        pass
