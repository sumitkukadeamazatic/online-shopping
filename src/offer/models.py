from django.db import models
from user import models as user_model
from order import models as order_model
from product import models as product_model
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Offer(models.Model):
    name            = models.CharField(max_length = 50)
    slug            = models.SlugField()
    description     = models.TextField()
    code            = models.CharField(max_length = 20,blank=True,null=True)
    amount          = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    percentage      = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    is_for_order    = models.BooleanField()
    minimum         = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    amount_limit    =  models.DecimalField( max_digits=5, decimal_places=2,blank=True,null=True)
    for_new_user    = models.BooleanField()
    valid_from      = models.DateTimeField(blank=True,null=True)
    valid_upto      = models.DateTimeField(blank=True,null=True)
    start_time      = models.TimeField(blank=True,null=True)
    end_time        = models.TimeField(blank=True,null=True)
    days            = ArrayField(models.IntegerField(),blank=True,null=True)
    max_count       = models.IntegerField(blank=True,null=True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at','valid_from','valid_upto','name'], name='offer_index')
        ]

class ProductOffer(models.Model):
    product_id  = models.ForeignKey(product_model.Product,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'product_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='product_offer_index')
        ]

class OrderOffer(models.Model):
    order_id    = models.ForeignKey(order_model.Order,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'order_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='order_offer_index')
        ]

class UserOffer(models.Model):
    order_id    = models.ForeignKey(user_model.User,on_delete=models.CASCADE,related_name=None)
    offers_id   = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name=None)
    is_redeemed = models.BooleanField()
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'user_offer'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='user_offer_index')
        ]

