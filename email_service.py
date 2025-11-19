"""
PowerAI Email Service
Handles sending password reset emails and other notifications
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        """Initialize email service with configuration from environment variables"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.app_name = "PowerAI Lesotho"
        self.app_url = os.getenv('APP_URL', 'https://powerai-lesotho.streamlit.app')
    
    def _validate_config(self) -> tuple[bool, str]:
        """Validate email configuration"""
        if not self.sender_email:
            return False, "SENDER_EMAIL not configured"
        if not self.sender_password:
            return False, "SENDER_PASSWORD not configured"
        return True, "Configuration valid"
    
    def send_email(self, to_email: str, subject: str, html_body: str, 
                   text_body: Optional[str] = None) -> dict:
        """Send an email"""
        # Validate configuration
        is_valid, msg = self._validate_config()
        if not is_valid:
            logger.warning(f"Email not configured: {msg}")
            return {
                "success": False, 
                "message": f"Email service not configured. Please contact support at hlomohangsethuntsa3@gmail.com",
                "demo_mode": True
            }
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.app_name} <{self.sender_email}>"
            message["To"] = to_email
            
            # Add plain text version if provided
            if text_body:
                part1 = MIMEText(text_body, "plain")
                message.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_body, "html")
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return {"success": True, "message": "Email sent successfully"}
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed")
            return {
                "success": False,
                "message": "Email authentication failed. Please check email configuration."
            }
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}"
            }
    
    def send_password_reset_email(self, to_email: str, username: str, 
                                   reset_token: str) -> dict:
        """Send password reset email"""
        reset_link = f"{self.app_url}?reset_token={reset_token}"
        
        subject = f"{self.app_name} - Password Reset Request"
        
        # HTML version
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #2c5530, #4a7c59);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    padding: 15px 30px;
                    background: #2c5530;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 0.9em;
                }}
                .warning {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ {self.app_name}</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Hello {username},</h2>
                    
                    <p>We received a request to reset your password for your {self.app_name} account.</p>
                    
                    <p>Click the button below to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </div>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px;">
                        {reset_link}
                    </p>
                    
                    <div class="warning">
                        <strong>⚠️ Important:</strong>
                        <ul>
                            <li>This link will expire in <strong>1 hour</strong></li>
                            <li>If you didn't request this, please ignore this email</li>
                            <li>Your password won't change until you create a new one</li>
                        </ul>
                    </div>
                    
                    <p>If you have any questions, contact us at 
                       <a href="mailto:hlomohangsethuntsa3@gmail.com">hlomohangsethuntsa3@gmail.com</a>
                    </p>
                    
                    <div class="footer">
                        <p>© 2025 {self.app_name} | UN SDG 7 Compliant Energy Management</p>
                        <p>This is an automated email, please do not reply.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        {self.app_name} - Password Reset Request
        
        Hello {username},
        
        We received a request to reset your password for your {self.app_name} account.
        
        Click the link below to reset your password:
        {reset_link}
        
        IMPORTANT:
        - This link will expire in 1 hour
        - If you didn't request this, please ignore this email
        - Your password won't change until you create a new one
        
        If you have any questions, contact us at hlomohangsethuntsa3@gmail.com
        
        © 2025 {self.app_name}
        This is an automated email, please do not reply.
        """
        
        return self.send_email(to_email, subject, html_body, text_body)
    
    def send_welcome_email(self, to_email: str, username: str, 
                          company_name: str) -> dict:
        """Send welcome email to new users"""
        subject = f"Welcome to {self.app_name}! 🎉"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #2c5530, #4a7c59);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .feature {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #2c5530;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ Welcome to {self.app_name}!</h1>
                </div>
                <div class="content">
                    <h2>Hello {username},</h2>
                    
                    <p>Thank you for registering <strong>{company_name}</strong> with {self.app_name}!</p>
                    
                    <p>You now have access to:</p>
                    
                    <div class="feature">
                        <strong>⚡ AI-Powered Forecasting</strong><br>
                        24-hour energy demand predictions
                    </div>
                    
                    <div class="feature">
                        <strong>📊 Real-time Monitoring</strong><br>
                        Live energy tracking and analytics
                    </div>
                    
                    <div class="feature">
                        <strong>💰 Cost Optimization</strong><br>
                        Maximize efficiency and reduce costs
                    </div>
                    
                    <div class="feature">
                        <strong>🌍 SDG 7 Compliance</strong><br>
                        Sustainable energy management
                    </div>
                    
                    <p style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <strong>🎁 Free Trial:</strong> You have 14 days of free access to all features!
                    </p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{self.app_url}" style="display: inline-block; padding: 15px 30px; 
                           background: #2c5530; color: white; text-decoration: none; border-radius: 5px;">
                            Launch Dashboard
                        </a>
                    </p>
                    
                    <p>Need help? Contact us at 
                       <a href="mailto:hlomohangsethuntsa3@gmail.com">hlomohangsethuntsa3@gmail.com</a>
                    </p>
                    
                    <p style="text-align: center; margin-top: 30px; color: #666; font-size: 0.9em;">
                        © 2025 {self.app_name} | UN SDG 7 Compliant
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_body)


if __name__ == "__main__":
    # Test email service
    service = EmailService()
    is_valid, msg = service._validate_config()
    
    if is_valid:
        print("✅ Email service configured correctly")
    else:
        print(f"⚠️  Email service not configured: {msg}")
        print("\nTo enable email functionality, set these environment variables:")
        print("  SENDER_EMAIL=your-email@gmail.com")
        print("  SENDER_PASSWORD=your-app-password")
        print("\nFor Gmail, create an App Password at:")
        print("  https://myaccount.google.com/apppasswords")
