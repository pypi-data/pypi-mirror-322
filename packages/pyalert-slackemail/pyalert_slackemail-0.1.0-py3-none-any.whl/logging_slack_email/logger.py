import logging
import requests
import smtplib
from email.mime.text import MIMEText

class Logger:
    def __init__(self, slack_webhook_url, email_settings):
        self.slack_webhook_url = slack_webhook_url
        self.email_settings = email_settings
        self.logger = logging.getLogger("SlackEmailLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def send_slack_notification(self, message):
        requests.post(self.slack_webhook_url, json={"text": message})
        

        
    def send_email_notification(self, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.email_settings['username']
        msg['To'] = self.email_settings['recipient']

        try:
            with smtplib.SMTP(self.email_settings['smtp_server'], self.email_settings['smtp_port']) as server:
                server.starttls()
                server.login(self.email_settings['username'], self.email_settings['password'])
                server.send_message(msg)
            return "Email sent successfully"
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return f"Failed to send email: {e}"

    def info(self, message):
        self.logger.info(message)
        self.send_slack_notification(message)
        self.send_email_notification("INFO: Log Notification", message)

    def warning(self, message):
        self.logger.warning(message)
        self.send_slack_notification(message)
        self.send_email_notification("WARNING: Log Notification", message)

    def error(self, message):
        self.logger.error(message)
        self.send_slack_notification(message)
        self.send_email_notification("ERROR: Log Notification", message)
