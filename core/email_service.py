from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_email(to_email, subject, body, is_html=False):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body if is_html else f'<p>{body}</p>'
    )

    client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    response = client.send(message)
    return response.status_code


def send_email_using_default_email(to_email, subject, body, html_message):
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],        
    )
    email.attach_alternative(html_message, "text/html")
    email.send()