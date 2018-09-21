"""
    serializers for product app
"""
from rest_framework import serializers, exceptions
from django.db.models import Avg, Max, Min
from .models import (User,
                     Product,
                     Category,
                     Wishlist,
                     Review,
                     ProductSeller,
                     ProductFeature,
                     Feature)
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    """
        serializers for product app
    """
    class Meta:
        '''meta'''
        model = Category
        fields = ('id', 'name', 'slug')

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    feature = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id',
                  'slug',
                  'name',
                  'rating',
                  'base_price',
                  'images',
                  'in_stock',
                  'feature',
                  'description',
                  'reviews')
    def get_rating(self, obj):
        return Review.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']

    def get_in_stock(self, obj):
        return sum(ProductSeller.objects.filter(product=obj).values_list('quantity', flat=True))
    
    def get_feature(self, obj):
        feature_list = Feature.objects.filter(category=obj.category)
        features = {}
        for feature_object in feature_list:
            try:
                feature_name = feature_object.name
                feature_value = ProductFeature.objects.filter(
                    feature=feature_object, product=obj).values_list('value', flat=True).get()
                features.update({feature_name : feature_value})
            except Exception:
                return ""

        return features
    
    def get_reviews(self, obj):
        return Review.objects.filter(product=obj).values('id',
                                                         'rating',
                                                         'user',
                                                         'title',
                                                         'description')



class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'product')

    def create(self, validate_data):
        return Wishlist.objects.create(user=self.context['request'].user, product=validate_data['product'])

class ProductSellerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    selling_exprience = serializers.SerializerMethodField()
    delivery_days = serializers.SerializerMethodField()

    class Meta:
        model = ProductSeller
        fields = ('id',
                  'name',
                  'rating',
                  'selling_price',
                  'selling_exprience',
                  'delivery_days')

    def get_name(self, obj):
        return obj.seller.company_name
    def get_rating(self, obj):
        return Review.objects.filter(seller=obj.seller).aggregate(Avg('rating'))['rating__avg']
    def get_selling_exprience(self, obj):
        return str(timezone.now().year - obj.created_at.year)+" years."
    def get_selling_price(self, obj):
        price = obj.selling_price
        discount = obj.discount
        sp = price - (price*(discount/100))
        return sp
    def get_delivery_days(self, obj):
        return {"min":obj.min_delivery_days,
                "max":obj.max_delivery_days}

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'title', 'description')

class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'seller', 'rating', 'title', 'description')
