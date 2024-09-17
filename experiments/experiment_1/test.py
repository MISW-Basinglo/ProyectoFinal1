import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ALLOWED_SENDERS = os.getenv("ALLOWED_SENDERS", "andrescercal@hotmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
TO_EMAIL = os.getenv("TO_EMAIL", "afelipe.cerquera@gmail.com")


def send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body, sender_email):
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish connection to the Hotmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade to secure connection
        server.login(smtp_user, smtp_password)  # Log in to Hotmail

        # Send email
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email} from {sender_email}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()


# Example usage
smtp_server = SMTP_SERVER
smtp_port = SMTP_PORT
smtp_user = ALLOWED_SENDERS
smtp_password = SMTP_PASSWORD

to_email = TO_EMAIL
subject = 'Correo incidente de prueba'
body = 'Este es un correo de prueba emulando ser un incidente.'

# Custom sender email and name (alias)
sender_email = smtp_user

# Call the function to send the email
if __name__ == "__main__":
    mails_to_send = 150
    print(f"Sending {mails_to_send} emails...")
    for _ in range(mails_to_send):
        send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body, sender_email)