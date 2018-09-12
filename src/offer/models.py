"""
        Configuration of Models
"""
from user import models as user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from order import models as order_model
from product import models as product_model
from utils.models import CustomBaseModelMixin
from rest_framework.exceptions import ValidationError
# Create your models here.


class Offer(CustomBaseModelMixin):
    """
    Configuration of OfferModel
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True)
    is_for_order = models.BooleanField()
    minimum = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True)
    amount_limit = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    for_new_user = models.BooleanField()
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_upto = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    days = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    max_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'valid_from',
                    'valid_upto',
                    'name'],
                name='offer_index')]

    def __str__(self):
        return self.name


class ProductOffer(CustomBaseModelMixin):
    """
        Configuration of ProductOfferModel
    """
    product = models.ForeignKey(
        product_model.Product,
        on_delete=models.CASCADE,
        related_name=None)
    offers = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)


class OrderOffer(CustomBaseModelMixin):
    """
        Configuration of OrderOfferModel
    """
    order = models.ForeignKey(
        order_model.Order,
        on_delete=models.CASCADE,
        related_name=None)
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)

    def validate_unique(self, exclude=None):
        existing_relation = OrderOffer.objects.filter(
            order__id=self.order.id, offer__id=self.offer.id).first()
        if not existing_relation is None:
            raise ValidationError('Order-Offer relation already exists.')


class UserOffer(CustomBaseModelMixin):
    """
        Configuration of UserOfferModel
    """
    user = models.ForeignKey(
        user_model.User,
        on_delete=models.CASCADE,
        related_name=None)
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)
    is_redeemed = models.BooleanField(default=False)


class OfferLineitem(CustomBaseModelMixin):
    """
        Configuration of OfferLineitemModel
    """
    lineitem = models.ForeignKey(
        order_model.Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)
