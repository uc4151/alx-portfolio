# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender:
    def __init__(self):
        # The recipient (you) is always the same
        self.recipient = os.getenv("EMAIL_USER")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = os.getenv("SMTP_PORT", 587)
        
    def send_email(self, sender_email, sender_name, subject, body, body_html=None):
        """Send an email where the recipient is always the user (you) and the sender is the logged-in user."""
        try:
            # Create the MIME multipart message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = self.recipient
            
            # Attach plain text part
            text_part = MIMEText(body, "plain")
            msg.attach(text_part)

            # Attach HTML part if provided
            if body_html:
                html_part = MIMEText(body_html, "html")
                msg.attach(html_part)

            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                # No need to login the sender, just the server credentials
                server.login(self.recipient, os.getenv("EMAIL_PASS"))
                server.sendmail(sender_email, self.recipient, msg.as_string())
            
            print(f"Email sent successfully from {sender_name}!")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")

