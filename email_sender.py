import os
import smtplib
from email.message import EmailMessage
from database import get_latest_insights


def send_email_report(to_email):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError("Missing EMAIL_ADDRESS or EMAIL_PASSWORD")

    insights = get_latest_insights()

    email_body = "AI Daily Insight Report\n\n"

    for keyword, insight in insights:

        email_body += f"""
================================

{keyword.upper()}

{insight}

"""

    msg = EmailMessage()
    msg["Subject"] = "AI Daily Insight Report"
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.set_content(email_body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)