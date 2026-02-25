from django.db import models


class Organization(models.Model):
    """
    Represents an organization (tenant) in the system.
    Organizations own users, projects, and subscriptions.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
