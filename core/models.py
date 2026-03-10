from django_extensions.db.models import TimeStampedModel
from django.db import models

class BaseModel(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
