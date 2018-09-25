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
    parent_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        '''meta'''
        indexes = [
            models.Index(
                fields=[
                    'name',
                    'created_at',
                    'updated_at'],
                name='category_index'),
        ]

    def __str__(self):
        return self.name


class Feature(CustomBaseModelMixin):
    """
       This represents feature table in database.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        '''meta'''
        indexes = [
            models.Index(
                fields=[
                    'name',
                ],
                name='feature_index'),
        ]

    def __str__(self):
        return self.name


class Tax(CustomBaseModelMixin):
    """
       This represents tax table in database.
    """
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=50, unique=True)
    percent = ArrayField(models.DecimalField(max_digits=5, decimal_places=2))
    is_active = models.BooleanField()

    class Meta:
        '''meta'''
        indexes = [
            models.Index(
                fields=[
                    'name',
                ],
                name='tax_index'),
        ]

    def __str__(self):
        return self.name


class CategoryTax(CustomBaseModelMixin):
    """
       This represents category_tax table in database.
    """
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return self.tax.name


class Brand(CustomBaseModelMixin):
    """
       This represents brand table in database.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        '''meta'''
        indexes = [
            models.Index(
                fields=[
                    'name',
                ],
                name='brand_index'),
        ]

    def __str__(self):
        return self.name


class Product(CustomBaseModelMixin):
    """
       This represents product table in database.
    """
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    slug = models.SlugField(unique=True)
    images = ArrayField(models.TextField())

    class Meta:
        '''meta'''
        indexes = [
            models.Index(
                fields=[
                    'name',
                ],
                name='product_index'),
        ]

    def __str__(self):
        return self.name


class ProductFeature(CustomBaseModelMixin):
    """
       This represents product_feature table in database.
    """
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'value',
                ],
                name='product_feature_index'),
        ]

    def __str__(self):
        return self.feature.name + " of " + self.product.name


class ProductSeller(CustomBaseModelMixin):
    """
       This represents product_seller table in database.
    """
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
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
                ],
                name='product_seller_index'),
        ]

    def __str__(self):
        return self.seller.company_name+"-"+self.product.name


class Review(CustomBaseModelMixin):
    """
       This represents review table in database.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'rating',
                ],
                name='review_index')]


class Wishlist(CustomBaseModelMixin):
    """
       This represents wishlist table in database.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
