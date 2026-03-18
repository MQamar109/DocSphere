from django.db import models

from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
