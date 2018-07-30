from django.db import models
from user.models import User
from user import models as user_model
from seller.models import Seller
from django.contrib.postgres.fields import ArrayField

class Category(user_model.Create_update_date):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    parent_id = models.BigIntegerField(null=True)

    class Meta:
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='category_index'),
                  ]
        db_table = 'catgory'

class Feature(user_model.Create_update_date):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='feature_index'),
                  ]
        db_table = 'feature' 

class Tax(user_model.Create_update_date):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=50)
    percent = ArrayField(models.DecimalField(max_digits=5, decimal_places=2))
    is_active = models.BooleanField()

    class Meta:
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='tax_index'),
                  ]
        db_table = 'tax'

class CategoryTax(user_model.Create_update_date):
    tax_id = models.ForeignKey(Tax,on_delete=models.CASCADE)
    category_id  = models.ForeignKey(Category,on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default="")

    class Meta:
        indexes = [
                    models.Index(fields=['created_at','updated_at'], name='category_tax_index'),
                  ]
        db_table = 'category_tax'



class Brand(user_model.Create_update_date):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='brand_index'),
                  ]
        db_table='brand'
 
    

class Product(user_model.Create_update_date):
    brand_id = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category_id  = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TimeField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    slug = models.CharField(max_length=50)
    images = ArrayField(models.TextField())
    

    class Meta: 
        indexes = [
                    models.Index(fields=['name','created_at','updated_at'], name='product_index'),
                  ]
        db_table = 'product'


class ProductFeature(user_model.Create_update_date):
    feature_id = models.ForeignKey(Feature,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    value = models.CharField(max_length=50)


    class Meta:
        indexes = [
                    models.Index(fields=['value','created_at','updated_at'], name='product_feature_index'),
                  ]
        db_table='product_feature'

       


class ProductSeller(user_model.Create_update_date):
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    min_delivery_days = models.PositiveSmallIntegerField()
    max_delivery_days = models.PositiveSmallIntegerField()
    available_pin_codes = ArrayField(models.CharField(max_length=10))
    is_default = models.BooleanField()

    class Meta:
        indexes = [
                    models.Index(fields=['discount','max_delivery_days','min_delivery_days','created_at','updated_at'], name='product_seller_index'),
                  ]
        db_table = 'product_seller'



class Review(user_model.Create_update_date):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2)
    title = models.CharField(max_length = 50, null = True)
    description = models.TextField(null = True)

    class Meta():
        db_table = 'review'
        indexes = [
            models.Index(fields = ['rating', 'created_at', 'updated_at'], name = 'review_index')
        ]


class Wishlist(user_model.Create_update_date):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    class Meta():
        db_table = 'wishlist'
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name = 'wishlist_index')
        ]

