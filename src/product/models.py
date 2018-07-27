from django.db import models
from user.models import User
from seller.models import Seller
from django.contrib.postgres.fields import ArrayField
from seller.models import Product

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    parent_id = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catgory'
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='category_index'),
                  ]

class Feature(models.Model):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feature' 
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='feature_index'),
                  ]

class Tax(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=50)
    percent = ArrayField(models.DecimalField(max_digits=5, decimal_places=2))
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tax'
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='tax_index'),
                  ]

class CategoryTax(models.Model):
    tax_id = models.ForeignKey(Tax,on_delete=models.CASCADE)
    category_id  = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'category_tax'
        indexes = [
                    models.Index(fields=['created_at','updated_at'], name='category_tax_index'),
                  ]



class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='brand'
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='brand_index'),
                  ]
 
    

class Product(models.Model):
    brand_id = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category_id  = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TimeField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    slug = models.CharField(max_length=50)
    images = ArrayField(models.TextField())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta: 
        db_table = 'product'
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='product_index'),
                  ]


class ProductFeature(models.Model):
    feature_id = models.ForeignKey(Feature,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table='product_feature'
        indexes = [
                    models.Index(fields=['value','created_at','updated_at'], name='product_feature_index'),
                  ]

       


class ProductSeller(models.Model):
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    min_delivery_days = models.PositiveSmallIntegerField()
    max_delivery_days = models.PositiveSmallIntegerField()
    available_pin_codes = ArrayField(models.CharField(max_length=10))
    is_default = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_seller'
        indexes = [
                    models.Index(fields=['discount','max_delivery_days','min_delivery_days','created_at','updated_at'], name='product_seller_index'),
                  ]



class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2)
    title = models.CharField(max_length = 50, null = True)
    description = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'review'
        indexes = [
            models.Index(fields = ['rating', 'created_at', 'updated_at'], name = 'review_index')
        ]


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'wishlist'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name = 'wishlist_index')
        ]

