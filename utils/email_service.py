import os
import html
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "hariniportfolio.contact@gmail.com"


def send_contact_email(name, sender_email, subject, message):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)

        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=FROM_EMAIL,
            subject=f"Portfolio Contact: {subject}",
            html_content=f"""
            <h3>New Contact Form</h3>
            <p><b>Name:</b> {html.escape(name)}</p>
            <p><b>Email:</b> {html.escape(sender_email)}</p>
            <p><b>Message:</b><br>{html.escape(message)}</p>
            """
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

        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipient_email,
            subject="Thanks for contacting me!",
            html_content=f"""
            <p>Hi {html.escape(name)},</p>
            <p>Thanks for reaching out. I received your message about <b>{html.escape(subject)}</b>.</p>
            <p>I’ll reply soon.</p>
            <p>— Harini</p>
            """
        )

        sg.send(mail)
        print("✅ Acknowledgement email sent")
        return True

    except Exception as e:
        print("❌ SendGrid acknowledgement failed:", e)
        return False
