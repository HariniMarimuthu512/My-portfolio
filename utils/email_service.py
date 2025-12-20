import os
import html
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Must exist in Render Environment Variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# MUST be a verified sender in SendGrid
FROM_EMAIL = "hariniportfolio.contact@gmail.com"


def send_contact_email(name, sender_email, subject, message):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background:#f9fafb; padding:20px;">
            <div style="max-width:600px;margin:auto;background:white;padding:20px;border-radius:8px;">
              <h2 style="color:#4f46e5;">📩 New Contact Form</h2>
              <p><b>Name:</b> {html.escape(name)}</p>
              <p><b>Email:</b> {html.escape(sender_email)}</p>
              <p><b>Message:</b></p>
              <p style="background:#f1f5f9;padding:12px;border-radius:6px;">
                {html.escape(message)}
              </p>
            </div>
          </body>
        </html>
        """

        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=FROM_EMAIL,
            subject=f"Portfolio Contact: {subject}",
            plain_text_content=f"""
New Contact Form

Name: {name}
Email: {sender_email}
Message:
{message}
""",
            html_content=html_body
        )

        sg.send(mail)
        print("✅ Submission email sent")
        return True

    except Exception as e:
        print("❌ SendGrid submission failed:", e)
        return False


def send_acknowledgement_email(name, recipient_email, subject):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background:#f9fafb; padding:20px;">
            <div style="max-width:600px;margin:auto;background:white;padding:20px;border-radius:8px;">
              <h2 style="color:#10b981;">✅ Message Received</h2>
              <p>Hi <b>{html.escape(name)}</b>,</p>
              <p>
                Thanks for reaching out regarding
                <b>{html.escape(subject)}</b>.
              </p>
              <p>I’ll get back to you shortly.</p>
              <p style="margin-top:20px;">— Harini</p>
            </div>
          </body>
        </html>
        """

        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipient_email,
            subject="Thanks for contacting me!",
            plain_text_content=f"""
Hi {name},

Thanks for reaching out regarding {subject}.
I’ll reply soon.

— Harini
""",
            html_content=html_body
        )

        sg.send(mail)
        print("✅ Acknowledgement email sent")
        return True

    except Exception as e:
        print("❌ SendGrid acknowledgement failed:", e)
        return False
