"""
product app models
"""

from user.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from utils.models import CustomBaseModelMixin
from seller.models import Seller


class Category(CustomBaseModelMixin):
    """
       This represents catgory table in database.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    parent_id = models.BigIntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='category_index'),
        ]


class Feature(CustomBaseModelMixin):
    """
       This represents feature table in database.
    """
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='feature_index'),
        ]


class Tax(CustomBaseModelMixin):
    """
       This represents tax table in database.
    """
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=50, unique=True)
    percent = ArrayField(models.DecimalField(max_digits=5, decimal_places=2))
    is_active = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='tax_index'),
        ]


class CategoryTax(CustomBaseModelMixin):
    """
       This represents category_tax table in database.
    """
    tax_id = models.ForeignKey(Tax, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='category_tax_index'),
        ]


class Brand(CustomBaseModelMixin):
    """
       This represents brand table in database.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='brand_index'),
        ]


class Product(CustomBaseModelMixin):
    """
       This represents product table in database.
    """
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    slug = models.SlugField(unique=True)
    images = ArrayField(models.TextField())

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='product_index'),
        ]


class ProductFeature(CustomBaseModelMixin):
    """
       This represents product_feature table in database.
    """
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'value',
                    'created_at',
                    'updated_at'],
                name='product_feature_index'),
        ]


class ProductSeller(CustomBaseModelMixin):
    """
       This represents product_seller table in database.
    """
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    min_delivery_days = models.PositiveSmallIntegerField()
    max_delivery_days = models.PositiveSmallIntegerField()
    available_pin_codes = ArrayField(models.CharField(max_length=10))
    is_default = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'discount',
                    'max_delivery_days',
                    'min_delivery_days',
                    'created_at',
                    'updated_at'],
                name='product_seller_index'),
        ]


class Review(CustomBaseModelMixin):
    """
       This represents review table in database.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'rating',
                    'created_at',
                    'updated_at'],
                name='review_index')]


class Wishlist(CustomBaseModelMixin):
    """
       This represents wishlist table in database.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='wishlist_index')]
