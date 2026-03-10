from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel
from .choices import USER_ROLE_OPTIONS
from .userManager import UserManager


class User(AbstractUser, BaseModel):
    """
    Custom user model child of AbstractUser. Authenticates with email, belongs to one organization,
    and has a role (admin, manager, or user) within that organization.
    """

    email = models.EmailField(unique=True)
    role = models.CharField(choices=USER_ROLE_OPTIONS, max_length=7, default="user")

    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    username = None
    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
