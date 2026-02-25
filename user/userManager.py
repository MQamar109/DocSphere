from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom manager for the User model. Handles creation of normal users and
    superusers using email (not username). Normalizes email and hashes passwords.
    """

    def create_user(self, email, password=None, **extra_fields):        
        if not email:
            raise ValueError('Email is required')
            
        email =self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)
