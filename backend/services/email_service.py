"""
Email Service for Reputation Guardian
Supports multiple email providers: SMTP, SendGrid, AWS SES
"""

import os
from typing import Dict, Optional
from datetime import datetime


class EmailService:
    """
    Unified email service supporting multiple providers
    """
    
    def __init__(self):
        self.provider = os.getenv('EMAIL_PROVIDER', 'smtp').lower()
        self.from_email = os.getenv('EMAIL_FROM', 'noreply@reputationguardian.com')
        self.from_name = os.getenv('EMAIL_FROM_NAME', 'Reputation Guardian')
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send email using configured provider
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text fallback (optional)
            
        Returns:
            bool: True if sent successfully
        """
        try:
            if self.provider == 'sendgrid':
                return self._send_via_sendgrid(to_email, subject, html_content, text_content)
            elif self.provider == 'smtp':
                return self._send_via_smtp(to_email, subject, html_content, text_content)
            elif self.provider == 'aws_ses':
                return self._send_via_ses(to_email, subject, html_content, text_content)
            else:
                # Fallback: just print to console for development
                return self._send_via_console(to_email, subject, html_content)
                
        except Exception as e:
            print(f"❌ Email send failed: {str(e)}")
            return False
    
    def _send_via_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str]
    ) -> bool:
        """Send email via SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            api_key = os.getenv('SENDGRID_API_KEY')
            if not api_key:
                raise ValueError("SENDGRID_API_KEY not set in environment")
            
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                message.plain_text_content = Content("text/plain", text_content)
            
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            print(f"✅ Email sent via SendGrid to {to_email} (Status: {response.status_code})")
            return True
            
        except ImportError:
            print("⚠️ SendGrid library not installed. Run: pip install sendgrid")
            return self._send_via_console(to_email, subject, html_content)
        except Exception as e:
            print(f"❌ SendGrid error: {str(e)}")
            return False
    
    def _send_via_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str]
    ) -> bool:
        """Send email via SMTP (Gmail, etc.)"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USERNAME')
            smtp_pass = os.getenv('SMTP_PASSWORD')
            
            if not smtp_user or not smtp_pass:
                raise ValueError("SMTP credentials not set in environment")
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            # Send via SMTP
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(message)
            
            print(f"✅ Email sent via SMTP to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ SMTP error: {str(e)}")
            return False
    
    def _send_via_ses(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str]
    ) -> bool:
        """Send email via AWS SES"""
        try:
            import boto3
            
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            
            client = boto3.client('ses', region_name=aws_region)
            
            body = {'Html': {'Data': html_content}}
            if text_content:
                body['Text'] = {'Data': text_content}
            
            response = client.send_email(
                Source=f"{self.from_name} <{self.from_email}>",
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': body
                }
            )
            
            print(f"✅ Email sent via AWS SES to {to_email} (MessageId: {response['MessageId']})")
            return True
            
        except ImportError:
            print("⚠️ boto3 library not installed. Run: pip install boto3")
            return self._send_via_console(to_email, subject, html_content)
        except Exception as e:
            print(f"❌ AWS SES error: {str(e)}")
            return False
    
    def _send_via_console(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> bool:
        """
        Development mode: Print email to console instead of sending
        Useful for testing without email configuration
        """
        print("\n" + "="*80)
        print("📧 EMAIL (Console Mode - Not Actually Sent)")
        print("="*80)
        print(f"To: {to_email}")
        print(f"From: {self.from_name} <{self.from_email}>")
        print(f"Subject: {subject}")
        print(f"Time: {datetime.now().isoformat()}")
        print("-"*80)
        print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
        print("="*80 + "\n")
        return True


# Singleton instance
_email_service = None


def get_email_service() -> EmailService:
    """Get or create email service instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


def send_onboarding_email(
    to_email: str,
    offer_details: Dict,
    portal_link: str,
    payment_link: str
) -> bool:
    """
    Send comprehensive onboarding email to user
    
    This is called after admin creates a subscription offer
    """
    service = get_email_service()
    
    # Create HTML email content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; }}
            .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .price {{ font-size: 36px; font-weight: bold; color: #667eea; margin: 20px 0; }}
            .button {{ display: inline-block; padding: 15px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            .features {{ list-style: none; padding: 0; }}
            .features li {{ padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
            .features li:before {{ content: "✓ "; color: #10b981; font-weight: bold; }}
            .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Welcome to Reputation Guardian</h1>
                <p>Your Application Has Been Approved!</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>Your Subscription Details</h2>
                    <p><strong>Plan:</strong> {offer_details.get('tier', 'Custom').title()}</p>
                    <div class="price">${offer_details.get('final_price', 0):,.2f}/month</div>
                    {f'<p style="color: #10b981;">✨ {offer_details.get("discount_percent", 0)}% Discount Applied!</p>' if offer_details.get('discount_percent', 0) > 0 else ''}
                </div>
                
                <div class="section">
                    <h3>✨ Included Features</h3>
                    <ul class="features">
                        {''.join(f'<li>{feature}</li>' for feature in offer_details.get('features', []))}
                    </ul>
                </div>
                
                <div class="section">
                    <h3>🔐 Complete Your Onboarding</h3>
                    <p>To activate your protection, please complete these two steps:</p>
                    
                    <p><strong>Step 1: Secure Onboarding Portal</strong></p>
                    <p>Upload your documents, photos, and video introduction:</p>
                    <a href="{portal_link}" class="button">Access Onboarding Portal</a>
                    
                    <p style="margin-top: 30px;"><strong>Step 2: Payment Setup</strong></p>
                    <p>Set up your monthly subscription payment:</p>
                    <a href="{payment_link}" class="button">Set Up Payment</a>
                </div>
                
                <div class="section">
                    <h3>⏰ Timeline</h3>
                    <ul>
                        <li>Complete onboarding within 7 days</li>
                        <li>Protection starts within 24 hours of payment setup</li>
                        <li>First monitoring report within 48 hours</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h3>🔒 Security & Privacy</h3>
                    <p>All uploads are encrypted end-to-end with AES-256 encryption. Your information is never shared and is protected by enterprise-grade security.</p>
                </div>
                
                <div class="section">
                    <h3>❓ Questions?</h3>
                    <p>Reply to this email or call us:</p>
                    <p>📞 +1 (800) 555-GUARD</p>
                    <p>📧 onboarding@reputationguardian.com</p>
                </div>
            </div>
            
            <div class="footer">
                <p>This offer expires in 7 days: {offer_details.get('expires_at', 'N/A')}</p>
                <p>© 2025 Reputation Guardian. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text fallback
    text_content = f"""
    Welcome to Reputation Guardian!
    
    Your Application Has Been Approved
    
    Subscription Details:
    - Plan: {offer_details.get('tier', 'Custom').title()}
    - Monthly Investment: ${offer_details.get('final_price', 0):,.2f}
    {f"- Discount Applied: {offer_details.get('discount_percent', 0)}%" if offer_details.get('discount_percent', 0) > 0 else ''}
    
    Complete Your Onboarding:
    
    1. Onboarding Portal: {portal_link}
    2. Payment Setup: {payment_link}
    
    Questions? Contact us at onboarding@reputationguardian.com
    
    This offer expires in 7 days.
    """
    
    return service.send_email(
        to_email=to_email,
        subject="🛡️ Welcome to Reputation Guardian - Complete Your Onboarding",
        html_content=html_content,
        text_content=text_content
    )
