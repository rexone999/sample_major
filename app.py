# send_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(recipient_email, timestamps):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    
    # Email content
    subject = "Violence Detection Alert"
    body = "Violence detected at the following timestamps:\n" + "\n".join([f"{t:.2f} seconds" for t in timestamps])

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Set up the server and send the email
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()  # Encrypts the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
