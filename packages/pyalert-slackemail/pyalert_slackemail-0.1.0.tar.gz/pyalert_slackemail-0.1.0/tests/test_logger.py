# tests/test_logger.py

import unittest
from unittest.mock import patch, MagicMock
from logging_slack_email.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(
            slack_webhook_url='https://hooks.slack.com/your_end_point',
            email_settings={
                'smtp_server': 'smtp.example.com',
                'smtp_port': 587,
                'username': 'your_email@example.com',
                'password': 'your_password',
                'recipient': 'receiver_email@example.com'
            }
        )

    @patch('logging_slack_email.logger.requests.post')
    @patch('logging_slack_email.logger.smtplib.SMTP')
    def test_info_logging(self, mock_smtp, mock_post):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
        with self.assertLogs(self.logger.logger, level='INFO') as log:
            self.logger.info("Test info message")
            self.assertIn("Test info message", log.output[0])
            mock_post.assert_called_once()  # Check if Slack notification was sent
            mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()  # Check if email was sent

    @patch('logging_slack_email.logger.requests.post')
    @patch('logging_slack_email.logger.smtplib.SMTP')
    def test_warning_logging(self, mock_smtp, mock_post):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
        with self.assertLogs(self.logger.logger, level='WARNING') as log:
            self.logger.warning("Test warning message")
            self.assertIn("Test warning message", log.output[0])
            mock_post.assert_called_once()  # Check if Slack notification was sent
            mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()  # Check if email was sent

    @patch('logging_slack_email.logger.requests.post')
    @patch('logging_slack_email.logger.smtplib.SMTP')
    def test_error_logging(self, mock_smtp, mock_post):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
        with self.assertLogs(self.logger.logger, level='ERROR') as log:
            self.logger.error("Test error message")
            self.assertIn("Test error message", log.output[0])
            mock_post.assert_called_once()  # Check if Slack notification was sent
            mock_smtp.return_value.__enter__.return_value.send_message.assert_called_once()  # Check if email was sent

if __name__ == '__main__':
    unittest.main()