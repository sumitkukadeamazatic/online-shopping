"""
    Utils App Models.
"""
from django.db import models

# Create your models here.


class CustomBaseModelMixin(models.Model):
    """
       Abstract model class for Timestamps
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
