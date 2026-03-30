from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel
from .choices import UserRole
from .userManager import UserManager


class User(AbstractUser, BaseModel):
    """
    Custom user model child of AbstractUser. Authenticates
    with email, belongs to one organization, and has a role
    (admin, manager, or user) within that organization.
    """

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=UserRole.choices, max_length=7, default=UserRole.USER
    )

    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    username = None
    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}".strip()
            or self.email
        )
    
    class Meta:
        ordering = ['-created']
