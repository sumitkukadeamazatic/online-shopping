"""
    Contact App models
"""

from user.models import User
from django.db import models
from utils.models import CustomBaseModelMixin
from seller.models import Seller

# Create your models here.


class Address(CustomBaseModelMixin):
    """
       Represents table 'address'. This table is for storing addresses of both 'user' and 'seller'
    """
    name = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None)
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None)
    address_line = models.TextField()
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    pincode = models.CharField(max_length=10)
    is_home = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'pincode',
                    'state',
                    'city',
                ],
                name='address_index')]

    def original_name(self):
        """
            Returns the name of owner of that address, because address can be of user's or a seller's
        """
        if self.user_id is None:
            return self.seller.company_name
        return '%s %s' % (self.user.first_name, self.user.last_name)
