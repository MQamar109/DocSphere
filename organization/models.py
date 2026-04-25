from django.db import models
from django.utils.text import slugify

from core.models import BaseModel


class Organization(BaseModel):
    """
    Represents an organization (tenant) in the system.
    Organizations own users, projects, and subscriptions.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    admin_email = models.EmailField(unique=True)
    slug = models.SlugField(unique=True, blank=True)

    @property
    def email(self):
        """djstripe Customer.create reads subscriber.email; we store billing contact as admin_email."""
        return self.admin_email

    def __str__(self):
        return self.name
    
    def get_subscription(self):
        """
        Convenience method to get the active subscription for this org.
        Queries dj-stripe's table, not our own.
        """
        from djstripe.models import Subscription
        return Subscription.objects.filter(
            customer__subscriber_id=self.id,
            stripe_data__status__in=["active", "trialing"],
        ).first()

    def has_active_subscription(self):
        return self.get_subscription() is not None
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']