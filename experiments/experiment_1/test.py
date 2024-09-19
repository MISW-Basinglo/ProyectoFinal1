import os
import smtplib
import logging
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
        # Establish connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade to secure connection
        server.login(smtp_user, smtp_password)  # Log in

        # Send email
        server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email} from {sender_email}")
    except Exception as e:
        logging.error(f"Error: {e}")
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
sender_email = smtp_user

if __name__ == "__main__":
    mails_to_send = 150
    duration_seconds = 60
    start_time = time.time()

    for i in range(mails_to_send):
        email_start = time.time()

        send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body, sender_email)
        print(f"Email {i + 1}/{mails_to_send} sent")

        elapsed_time = time.time() - start_time

        remaining_time = duration_seconds - elapsed_time
        emails_left = mails_to_send - (i + 1)

        if emails_left > 0:
            interval = remaining_time / emails_left
            if interval > 0:
                time.sleep(interval)

    print(f"All emails sent.")
