import time

from experiments.experiment_1.src.services.pubsub_service import PubSubService
from experiments.experiment_1.src.utils import get_mail_service


class EmailDaemon:
    def __init__(self, poll_interval=60):
        self.mail_service = get_mail_service()
        self.pubsub_service = PubSubService()
        self.poll_interval = poll_interval  # Polling interval in seconds

    def is_valid_email(self, email_data):
        """Valida la estructura del correo para decidir si debe ser procesado o rechazado."""
        # Definir criterios básicos para validar el correo.
        subject = email_data.get("subject", "").lower()
        from_address = email_data.get("from", "").lower()
        body = email_data.get("body", "").lower()

        # Ejemplo de validaciones simples:

        # Regla 1: Rechazar correos que contengan palabras clave de spam en el asunto.
        spam_keywords = ['free', 'win', 'money', 'prize']
        if any(keyword in subject for keyword in spam_keywords):
            print(f"Correo rechazado por ser potencialmente spam. Asunto: {subject}")
            return False

        # Regla 2: Procesar solo correos de un remitente específico (para pruebas)
        allowed_senders = ['cliente@empresa.com']
        if from_address not in allowed_senders:
            print(f"Correo rechazado por remitente no autorizado: {from_address}")
            return False

        # Regla 3: Rechazar correos vacíos o con un cuerpo muy corto.
        if len(body) < 20:
            print(f"Correo rechazado por contenido insuficiente en el cuerpo.")
            return False

        # Si el correo cumple con todos los criterios, se considera válido.
        return True

    def run(self):
        print("Email daemon started.")
        while True:
            print("Pulling unread emails...")
            emails = self.mail_service.fetch_unread_emails()

            if emails:
                print(f"Fetched {len(emails)} unread emails.")
                for email in emails:
                    if self.is_valid_email(email):
                        # Publish each valid email to Pub/Sub
                        # self.pubsub_service.publish_message(str(email))
                        print("Correo publicado en Pub/Sub.")
                    else:
                        print(f"Correo descartado: {email.get('subject')}")
            else:
                print("No new emails found.")

            time.sleep(self.poll_interval)  # Wait for the next polling cycle
