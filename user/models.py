from django.db import models
from django.contrib.auth.models import AbstractUser
from .userManager import UserManager
from organization.models import Organization


class User(AbstractUser):
    """
    Custom user model child of AbstractUser. Authenticates with email, belongs to one organization,
    and has a role (admin, manager, or user) within that organization.
    """

    USER_ROLE_OPTIONS = [("admin","Admin"),('manager','Manager'), ("user","User")]

    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(choices=USER_ROLE_OPTIONS,max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    username = None 
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + " " + self.last_name
