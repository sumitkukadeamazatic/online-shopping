"""
    Seller App Models
"""
from user.models import User
from django.db import models
from utils.models import CustomBaseModelMixin


# Create your models here.


class Seller(CustomBaseModelMixin):
    """
       Represents table 'seller'
    """
    INPROGRESS = 'InProgress'
    ACTIVE = 'Active'
    INACTIVE = 'InActive'
    STATUS_CHOICES = (
        (INPROGRESS, 'InProgress'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'InActive'),
    )

    company_name = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=INPROGRESS)
    is_verified = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'company_name',
                ],
                name='seller_index')
        ]

    def __str__(self):
        return self.company_name


class SellerUser(CustomBaseModelMixin):
    """
       Seller and User relation table. (Many to Many Relationship)
    """
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
