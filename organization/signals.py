from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Organization
from core.email_service import send_email_using_default_email


@receiver(post_save, sender=Organization)
def send_organization_created_email(sender, instance, created, **kwargs):
    if not created:
        return

    subject = f"Organization created: {instance.name}"
    message = (
        f"Hello,\n\n"
        f"Your organization '{instance.name}' has been created successfully.\n"
        f"Slug: {instance.slug}\n\n"
        f"Thanks."
    )
    html_message = (
        "<html><body>"
        "<h2>Organization Created Successfully</h2>"
        f"<p>Your organization <strong>{instance.name}</strong> has been created.</p>"
        f"<p><strong>Slug:</strong> {instance.slug}</p>"
        "<p>Thanks.</p>"
        "</body></html>"
    )

    send_email_using_default_email(instance.admin_email, subject, message, html_message)
