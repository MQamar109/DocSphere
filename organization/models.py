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
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args, **kwargs)
