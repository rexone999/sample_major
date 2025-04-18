import smtplib
from email.mime.text import MIMEText

def send_email_alert(receiver_email, timestamps):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    body = "Violence detected at the following times (seconds):\n" + "\n".join([f"{t:.2f}" for t in timestamps])
    msg = MIMEText(body)
    msg["Subject"] = "Violence Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)