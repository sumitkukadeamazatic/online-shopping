from django.db import models
from utils.models import TimestampsAbstract
from user.models import User


# Create your models here.


class Seller(TimestampsAbstract):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    company_name = models.CharField(max_length = 50, unique=True)
    contact_number = models.CharField(max_length = 20)

    class Meta():
        db_table = 'seller'
        indexes = [
            models.Index(fields = ['company_name', 'created_at', 'updated_at'], name = 'seller_index')
        ]

        
class Address(TimestampsAbstract):
    name = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    address_line = models.TextField()
    city = models.CharField(max_length = 60)
    state = models.CharField(max_length = 60)
    pincode = models.CharField(max_length = 10)
    is_home = models.BooleanField(default = False)

    class Meta():
        db_table = 'address'
        indexes = [
            models.Index(fields = ['pincode', 'state', 'city', 'created_at', 'updated_at'], name = 'address_index')
        ]
