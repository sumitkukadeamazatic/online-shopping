from django.db import models

# Create your models here.


class TimestampsAbstract(models.Model):
    """
       Abstract model class for Timestamps
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        """
         Configuration class
        """
        abstract = True
