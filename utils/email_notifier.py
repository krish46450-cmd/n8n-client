# utils/email_notifier.py - Email Notification Utility
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import Config

class EmailNotifier:
    def __init__(self):
        self.config = Config()
        self.smtp_server = self.config.MAIL_SERVER
        self.smtp_port = self.config.MAIL_PORT
        self.username = self.config.MAIL_USERNAME
        self.password = self.config.MAIL_PASSWORD
        self.from_email = self.config.MAIL_DEFAULT_SENDER
        self.enabled = bool(self.username and self.password)

        if not self.enabled:
            logging.warning("Email notifications disabled - MAIL_USERNAME or MAIL_PASSWORD not configured")

    def send_ticket_created_notification(self, user_email, user_name, ticket_id, ticket_title):
        """Send email notification when a support ticket is created"""
        if not self.enabled:
            logging.info("Email notifications disabled, skipping notification")
            return False

        subject = f"Support Ticket Created: {ticket_id}"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc; border-radius: 10px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0;">Support Ticket Created</h1>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p>Hello {user_name},</p>

                        <p>Your support ticket has been successfully created. Our team will review it shortly.</p>

                        <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea;">
                            <p style="margin: 0;"><strong>Ticket ID:</strong> {ticket_id}</p>
                            <p style="margin: 10px 0 0 0;"><strong>Title:</strong> {ticket_title}</p>
                        </div>

                        <p>You will receive email notifications when:</p>
                        <ul>
                            <li>A support agent responds to your ticket</li>
                            <li>Your ticket status changes</li>
                            <li>Your ticket is resolved</li>
                        </ul>

                        <p>You can view your ticket status by logging into your account.</p>

                        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                            <em>This is an automated message from Windows Dump Analyzer. Please do not reply to this email.</em>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

        plain_body = f"""
        Support Ticket Created

        Hello {user_name},

        Your support ticket has been successfully created. Our team will review it shortly.

        Ticket ID: {ticket_id}
        Title: {ticket_title}

        You will receive email notifications when:
        - A support agent responds to your ticket
        - Your ticket status changes
        - Your ticket is resolved

        You can view your ticket status by logging into your account.

        This is an automated message from Windows Dump Analyzer. Please do not reply to this email.
        """

        return self._send_email(user_email, subject, html_body, plain_body)

    def send_ticket_update_notification(self, user_email, user_name, ticket_id, ticket_title, update_message, status):
        """Send email notification when a support ticket is updated"""
        if not self.enabled:
            return False

        subject = f"Support Ticket Updated: {ticket_id}"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc; border-radius: 10px;">
                    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h1 style="color: white; margin: 0;">Ticket Update</h1>
                    </div>

                    <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p>Hello {user_name},</p>

                        <p>Your support ticket has been updated.</p>

                        <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981;">
                            <p style="margin: 0;"><strong>Ticket ID:</strong> {ticket_id}</p>
                            <p style="margin: 10px 0;"><strong>Title:</strong> {ticket_title}</p>
                            <p style="margin: 10px 0 0 0;"><strong>Status:</strong> {status}</p>
                        </div>

                        <div style="background: #dbeafe; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0;"><strong>Update:</strong></p>
                            <p style="margin: 10px 0 0 0;">{update_message}</p>
                        </div>

                        <p>Log in to your account to view the full ticket details and respond if needed.</p>

                        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                            <em>This is an automated message from Windows Dump Analyzer. Please do not reply to this email.</em>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

        plain_body = f"""
        Support Ticket Updated

        Hello {user_name},

        Your support ticket has been updated.

        Ticket ID: {ticket_id}
        Title: {ticket_title}
        Status: {status}

        Update:
        {update_message}

        Log in to your account to view the full ticket details and respond if needed.

        This is an automated message from Windows Dump Analyzer. Please do not reply to this email.
        """

        return self._send_email(user_email, subject, html_body, plain_body)

    def _send_email(self, to_email, subject, html_body, plain_body):
        """Internal method to send email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            # Attach both plain text and HTML versions
            part1 = MIMEText(plain_body, 'plain')
            part2 = MIMEText(html_body, 'html')

            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logging.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logging.error(f"Error sending email to {to_email}: {str(e)}")
            return False
