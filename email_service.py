"""
Email service for sending contact form submissions
"""
import smtplib
import os
import html
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# Email configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
except (ValueError, TypeError):
    SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER", "hariniportfolio.contact@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "hariniportfolio.contact@gmail.com")

# Debug: Print email configuration status (without showing password)
print("=" * 60)
print("EMAIL SERVICE CONFIGURATION:")
print(f"SMTP_SERVER: {SMTP_SERVER}")
print(f"SMTP_PORT: {SMTP_PORT}")
print(f"EMAIL_USER: {EMAIL_USER}")
print(f"RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")
print(f"EMAIL_PASSWORD configured: {'Yes' if EMAIL_PASSWORD else 'No (check .env file)'}")
print("=" * 60)


def send_contact_email(
    name: str,
    sender_email: str,
    subject: str,
    message: str
) -> bool:
    """
    Send contact form submission to recipient email
    
    Args:
        name: Name of the person submitting the form
        sender_email: Email address of the sender
        subject: Subject of the message
        message: Message content
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = f"Portfolio Contact: {subject or 'No Subject'}"
        msg["Reply-To"] = sender_email
        
        # Create professional HTML email body
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .email-container {{
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .email-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            padding: 30px 20px;
            text-align: center;
        }}
        .email-header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .email-header p {{
            margin: 10px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .email-content {{
            padding: 30px 20px;
        }}
        .info-section {{
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .info-row {{
            margin: 15px 0;
            padding-bottom: 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        .info-row:last-child {{
            border-bottom: none;
            padding-bottom: 0;
        }}
        .info-label {{
            font-weight: 600;
            color: #667eea;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .info-value {{
            font-size: 16px;
            color: #333333;
            word-break: break-word;
        }}
        .info-value a {{
            color: #667eea;
            text-decoration: none;
        }}
        .info-value a:hover {{
            text-decoration: underline;
        }}
        .message-section {{
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 20px;
            margin: 20px 0;
        }}
        .message-label {{
            font-weight: 600;
            color: #667eea;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}
        .message-content {{
            font-size: 15px;
            color: #333333;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        .email-footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        .email-footer p {{
            margin: 5px 0;
        }}
        .reply-note {{
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 14px;
            color: #1976D2;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>📧 New Contact Form Submission</h1>
            <p>Portfolio Website Notification</p>
        </div>
        
        <div class="email-content">
            <div class="info-section">
                <div class="info-row">
                    <div class="info-label">Name</div>
                    <div class="info-value">{html.escape(str(name))}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Email Address</div>
                    <div class="info-value">
                        <a href="mailto:{html.escape(sender_email)}">{html.escape(sender_email)}</a>
                    </div>
                </div>
                <div class="info-row">
                    <div class="info-label">Subject</div>
                    <div class="info-value">{html.escape(str(subject or 'No Subject'))}</div>
                </div>
            </div>
            
            <div class="message-section">
                <div class="message-label">Message</div>
                <div class="message-content">{html.escape(str(message)).replace(chr(10), '<br>').replace(chr(13), '')}</div>
            </div>
            
            <div class="reply-note">
                💡 <strong>Quick Reply:</strong> You can reply directly to this email to respond to {html.escape(str(name))} at <a href="mailto:{html.escape(sender_email)}" style="color: #1976D2;">{html.escape(sender_email)}</a>
            </div>
        </div>
        
        <div class="email-footer">
            <p>This email was automatically sent from your portfolio contact form.</p>
            <p style="margin-top: 10px; color: #adb5bd;">© Portfolio - Harini</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach only HTML version (modern email clients support HTML)
        # Set content type to HTML
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)
        
        # Send email
        if not EMAIL_PASSWORD:
            print("=" * 60)
            print("WARNING: EMAIL_PASSWORD not set in .env file!")
            print("Email sending is disabled.")
            print("=" * 60)
            print("To enable email sending:")
            print("1. Go to: https://myaccount.google.com/apppasswords")
            print("2. Generate an App Password for 'Mail'")
            print("3. Copy the 16-character password")
            print("4. Add it to .env file: EMAIL_PASSWORD=your_app_password")
            print("5. Restart the server")
            print("=" * 60)
            return False
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("=" * 60)
        print("EMAIL AUTHENTICATION ERROR:")
        print(f"Error: {str(e)}")
        print("=" * 60)
        print("Possible issues:")
        print("1. Gmail App Password is incorrect")
        print("2. 2-Step Verification is not enabled")
        print("3. 'Less secure app access' needs to be enabled (if using regular password)")
        print("=" * 60)
        return False
    except Exception as e:
        print("=" * 60)
        print(f"ERROR SENDING EMAIL: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


def send_acknowledgement_email(
    name: str,
    recipient_email: str,
    subject: str
) -> bool:
    """
    Send acknowledgement email to the person who submitted the contact form
    
    Args:
        name: Name of the person who submitted the form
        recipient_email: Email address to send acknowledgement to
        subject: Subject of their original message
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = "Thank you for contacting me!"
        msg["Reply-To"] = EMAIL_USER
        
        # Create professional HTML acknowledgement email
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .email-container {{
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .email-header {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #ffffff;
            padding: 40px 20px;
            text-align: center;
        }}
        .email-header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .email-header .icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        .email-content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            color: #333333;
            margin-bottom: 20px;
        }}
        .message {{
            font-size: 16px;
            color: #555555;
            line-height: 1.8;
            margin: 20px 0;
        }}
        .highlight-box {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 4px solid #10b981;
            padding: 20px;
            margin: 30px 0;
            border-radius: 4px;
        }}
        .highlight-box p {{
            margin: 0;
            color: #065f46;
            font-size: 15px;
        }}
        .info-section {{
            background-color: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }}
        .info-row {{
            margin: 10px 0;
            font-size: 14px;
            color: #666666;
        }}
        .info-label {{
            font-weight: 600;
            color: #10b981;
            display: inline-block;
            min-width: 80px;
        }}
        .email-footer {{
            background-color: #f8f9fa;
            padding: 25px;
            text-align: center;
            font-size: 13px;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        .email-footer p {{
            margin: 5px 0;
        }}
        .signature {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }}
        .signature-name {{
            font-weight: 600;
            color: #333333;
            font-size: 16px;
            margin-bottom: 5px;
        }}
        .signature-title {{
            color: #666666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <div class="icon">✓</div>
            <h1>Thank You for Reaching Out!</h1>
        </div>
        
        <div class="email-content">
            <div class="greeting">
                <strong>Hi {html.escape(str(name))},</strong>
            </div>
            
            <div class="message">
                <p>Thank you for contacting me through my portfolio website! I've received your message and I'm excited to connect with you.</p>
            </div>
            
            <div class="highlight-box">
                <p>💬 <strong>Your message has been received!</strong> I'll review it and get back to you as soon as possible, typically within 24-48 hours.</p>
            </div>
            
            <div class="info-section">
                <div class="info-row">
                    <span class="info-label">Subject:</span>
                    <span>{html.escape(str(subject or 'General Inquiry'))}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status:</span>
                    <span style="color: #10b981; font-weight: 600;">✓ Received</span>
                </div>
            </div>
            
            <div class="message">
                <p>In the meantime, feel free to:</p>
                <ul style="color: #555555; line-height: 2;">
                    <li>Check out my <a href="https://github.com/HariniMarimuthu512" style="color: #10b981; text-decoration: none;">GitHub profile</a> for more projects</li>
                    <li>Connect with me on <a href="https://www.linkedin.com/in/harini-m-7a0901278" style="color: #10b981; text-decoration: none;">LinkedIn</a></li>
                    <li>Browse my portfolio website for more information</li>
                </ul>
            </div>
            
            <div class="signature">
                <div class="signature-name">Best regards,</div>
                <div class="signature-name">Harini Marimuthu</div>
                <div class="signature-title">Python Developer | Backend Development | AI/ML</div>
            </div>
        </div>
        
        <div class="email-footer">
            <p>This is an automated confirmation email.</p>
            <p style="margin-top: 10px; color: #adb5bd;">© Portfolio - Harini</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach HTML version
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)
        
        # Send email
        if not EMAIL_PASSWORD:
            print("=" * 60, flush=True)
            print("ERROR: EMAIL_PASSWORD not set - cannot send acknowledgement email", flush=True)
            print("=" * 60, flush=True)
            return False
        
        print(f"Sending acknowledgement email to {recipient_email}...", flush=True)
        sys.stdout.flush()
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✓ Acknowledgement email sent successfully to {recipient_email}", flush=True)
        sys.stdout.flush()
        return True
        
    except Exception as e:
        print("=" * 60, flush=True)
        print(f"ERROR sending acknowledgement email: {str(e)}", flush=True)
        print("=" * 60, flush=True)
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False

