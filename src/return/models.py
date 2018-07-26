from django.db import models
from django.utils import timezone

# Create your models here.

class ReturnOrder(models.Model):
#    id = models.BigAutoField(primary_key=True)
#    order_id = models.ForeignKey(Order)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'return_order'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_order_index'),]


class ReturnLineitem(models.Model):
#    return_order_id = models.ForeignKey(ReturnOrder)
#    lineitem_id = models.ForeignKey(Lineitem)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'return_lineitem'
        indexes = [models.Index(fields=['status','raeson','created_at','updated_at'],name='return_lineitem_index'),]


class ReturnOrderLog(models.Model):
    return_lineitem_id = models.ForeignKey(ReturnLineitem)
    status = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'return_order_log'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_order_log_index'),]

class ReturnLineitemShippingDetail(models.Model):
#    shipping_detail_id = models.ForeignKey(ShippingDetail)
    return_lineitem_id = models.ForeignKey(Lineitem)
    quantity = models.IntegerField()
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'return_lineitem_shipping_detail'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_lineitem_shipping_detail_index'),]

