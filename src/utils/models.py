"""
    Utils App Models.
"""
from django.db import models

# Create your models here.


class CustomBaseModelMixin(models.Model):
    """
       Abstract model class for Timestamps
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
