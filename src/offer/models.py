"""
        Configuration of Models
"""
from user import models as user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from order import models as order_model
from product import models as product_model
from utils.models import CustomBaseModelMixin

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
                    'created_at',
                    'updated_at',
                    'valid_from',
                    'valid_upto',
                    'name'],
                name='offer_index')]


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

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='product_offer_index')]


class OrderOffer(CustomBaseModelMixin):
    """
        Configuration of OrderOfferModel
    """
    order = models.ForeignKey(
        order_model.Order,
        on_delete=models.CASCADE,
        related_name=None)
    offers = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='order_offer_index')]


class UserOffer(CustomBaseModelMixin):
    """
        Configuration of UserOfferModel
    """
    order = models.ForeignKey(
        user_model.User,
        on_delete=models.CASCADE,
        related_name=None)
    offers = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)
    is_redeemed = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='user_offer_index')]


class OfferLineitem(CustomBaseModelMixin):
    """
        Configuration of OfferLineitemModel
    """
    lineitem = models.ForeignKey(
        order_model.Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    offers = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name=None)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='offer_lineitem_index')]
