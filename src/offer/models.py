#from django.db import models
from user import models as user_model
from order import models as order_model
from product import models as product_model
from django.contrib.postgres.fields import ArrayField
from utils.models import TimestampsAbstract
# Create your models here.

class Offer(TimestampsAbstract):
    name            = models.CharField(max_length = 50)
    slug            = models.SlugField(max_length=50, unique=True ,db_index=True)
    description     = models.TextField()
    code            = models.CharField(max_length = 20,blank=True,null=True)
    amount          = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    percentage      = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    is_for_order    = models.BooleanField()
    minimum         = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    amount_limit    = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    for_new_user    = models.BooleanField()
    valid_from      = models.DateTimeField(blank=True,null=True)
    valid_upto      = models.DateTimeField(blank=True,null=True)
    start_time      = models.TimeField(blank=True,null=True)
    end_time        = models.TimeField(blank=True,null=True)
    days            = ArrayField(models.PositiveIntegerField(),blank=True,null=True)
    max_count       = models.PositiveIntegerField(blank=True,null=True)

    class Meta():
        db_table = 'offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at','valid_from','valid_upto','name'], name='offer_index')
        ]

class ProductOffer(TimestampsAbstract):
    product_id  = models.ForeignKey(product_model.Product,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)

    class Meta():
        db_table = 'product_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='product_offer_index')
        ]

class OrderOffer(user_model.Create_update_date):
    order_id    = models.ForeignKey(order_model.Order,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)

    class Meta():
        db_table = 'order_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='order_offer_index')
        ]

class UserOffer(TimestampsAbstract):
    order_id    = models.ForeignKey(user_model.User,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)
    is_redeemed = models.BooleanField()

    class Meta():
        db_table = 'user_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='user_offer_index')
        ]

