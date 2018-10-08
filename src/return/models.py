"""Models
    All return related models
"""

from django.db import models
# from django.utils import timezone
# from seller import models as seller_model
# from user import models as user_model
from order import models as order_model
from utils.models import CustomBaseModelMixin


class Order(CustomBaseModelMixin):
    """ Model
        return_order model
    """
    GENERATED = 'G'
    PARTIALLY_COMPLETE = 'PC'
    COMPLETE = 'C'
    STATUS_CHOICES_FIELDS = (
        (GENERATED, 'Generated'),
        (PARTIALLY_COMPLETE, 'Partially Complete'),
        (COMPLETE, 'Complete')
    )

    order = models.ForeignKey(order_model.Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES_FIELDS, default=GENERATED)

    def save(self, **kwargs):  # pylint: disable=arguments-differ
        status = self.status
        if not any(status in _tuple for _tuple in self.STATUS_CHOICES_FIELDS):
            raise ValueError('Invalid status')
        super(Order, self).save(**kwargs)


class Lineitem(CustomBaseModelMixin):
    """ Model
        return_lineitem model
    """

    GENERATED = 'GN'
    IN_PROGRESS = 'IP'
    CANCELED = 'CN'
    REJECTED = 'RJ'
    COMPLETE = 'CM'

    STATUS_CHOICES_FIELDS = (
        (GENERATED, 'Generated'),
        (IN_PROGRESS, 'In Progress'),
        (CANCELED, 'Canceled'),
        (REJECTED, 'Rejected'),
        (COMPLETE, 'Complete')
    )

    return_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    lineitem = models.ForeignKey(
        order_model.Lineitem,
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES_FIELDS, default=GENERATED)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'status',
                    'reason'
                ],
                name='return_lineitem_index'),
        ]

    def save(self, **kwargs):  # pylint: disable=arguments-differ
        status = self.status
        if not any(status in _tuple for _tuple in self.STATUS_CHOICES_FIELDS):
            raise ValueError('Invalid status')
        super(Lineitem, self).save(**kwargs)


class OrderLog(CustomBaseModelMixin):
    """ Model
        return_order_log model
    """
    return_lineitem = models.ForeignKey(
        Lineitem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)


class LineitemShippingDetail(CustomBaseModelMixin):
    """ Model
        return_lineitem_shipping detail model
    """
    shipping_detail = models.ForeignKey(
        order_model.ShippingDetails,
        on_delete=models.CASCADE)
    return_lineitem = models.ForeignKey(
        Lineitem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
