from django.db import models
from django.utils import timezone
from seller import models as seller_model
from order import models as order_model
from user import models as user_model
from utils.models import TimestampsAbstract



class ReturnOrder(TimestampsAbstract):
    order_id = models.ForeignKey(order_model.Order,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'return_order'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_order_index'),]


class ReturnLineitem(TimestampsAbstract):
    return_order_id = models.ForeignKey(ReturnOrder,on_delete=models.CASCADE)
    lineitem_id = models.ForeignKey(order_model.Lineitem,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'return_lineitem'
        indexes = [models.Index(fields=['status','reason','created_at','updated_at'],name='return_lineitem_index'),]


class ReturnOrderLog(TimestampsAbstract):
    return_lineitem_id = models.ForeignKey(ReturnLineitem,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'return_order_log'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_order_log_index'),]

class ReturnLineitemShippingDetail(TimestampsAbstract):
    shipping_detail_id = models.ForeignKey(order_model.ShippingDetails,on_delete=models.CASCADE)
    return_lineitem_id = models.ForeignKey(ReturnLineitem,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'return_lineitem_shipping_detail'
        indexes = [models.Index(fields=['created_at','updated_at'],name='return_lineitem_shipp_dtl_idx'),]

