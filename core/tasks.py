from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone


@shared_task(
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_default_email_task(to_email, subject, body, html_message):
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()


@shared_task(ignore_result=True)
def log_active_users():
    from user.models import User
    count = User.objects.filter(is_active=True).count()
    print(f"[{timezone.now()}] Active users: {count}")