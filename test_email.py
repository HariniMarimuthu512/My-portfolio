"""
Test script to check email configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("EMAIL CONFIGURATION CHECK")
print("=" * 60)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "hariniportfolio.contact@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "hariniportfolio.contact@gmail.com")

print(f"SMTP Server: {SMTP_SERVER}")
print(f"SMTP Port: {SMTP_PORT}")
print(f"Email User: {EMAIL_USER}")
print(f"Recipient Email: {RECIPIENT_EMAIL}")
print(f"Email Password Set: {'YES' if EMAIL_PASSWORD else 'NO'}")
print(f"Password Length: {len(EMAIL_PASSWORD)} characters")

if not EMAIL_PASSWORD:
    print("\n" + "=" * 60)
    print("PROBLEM FOUND: EMAIL_PASSWORD is not set!")
    print("=" * 60)
    print("\nTo fix this:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Generate an App Password for 'Mail'")
    print("3. Copy the 16-character password")
    print("4. Edit .env file and add: EMAIL_PASSWORD=your_password_here")
    print("5. Remove all spaces from the password")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("✓ Email password is configured")
    print("=" * 60)
    print("\nTesting email connection...")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create test message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "Test Email from Portfolio"
        
        body = "This is a test email from your portfolio website."
        msg.attach(MIMEText(body, "plain"))
        
        # Try to connect and send
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print("Starting TLS...")
            server.starttls()
            print("Logging in...")
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            print("Sending test email...")
            server.send_message(msg)
            print("\n✓ Test email sent successfully!")
            print(f"Check your inbox at: {RECIPIENT_EMAIL}")
            
    except smtplib.SMTPAuthenticationError as e:
        print("\n" + "=" * 60)
        print("AUTHENTICATION ERROR")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print("\nPossible issues:")
        print("1. Gmail App Password is incorrect")
        print("2. 2-Step Verification is not enabled")
        print("3. Password has spaces (remove them)")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"ERROR: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()

