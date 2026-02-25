from django.db import models
from django.contrib.auth.models import AbstractUser
from .userManager import UserManager
from .choices import USER_ROLE_OPTIONS


class User(AbstractUser):
    """
    Custom user model child of AbstractUser. Authenticates with email, belongs to one organization,
    and has a role (admin, manager, or user) within that organization.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices=USER_ROLE_OPTIONS,max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)

    USERNAME_FIELD = "email"
    username = None 
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + " " + self.last_name
