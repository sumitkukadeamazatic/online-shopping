"""
    serializers for product app
"""
from django.utils import timezone
from django.db.models import Avg
from rest_framework import serializers
from .models import (Product,
                     Category,
                     Wishlist,
                     Review,
                     ProductSeller,
                     ProductFeature,
                     Feature)


class CategorySerializer(serializers.ModelSerializer):
    """
        serializers for product app
    """
    class Meta:
        '''meta'''
        model = Category
        fields = ('id', 'name', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    '''
    Product Seller Serializer
    '''
    rating = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    feature = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        '''meta'''
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
        '''rating'''
        return Review.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']

    def get_in_stock(self, obj):
        '''check all stock from all seller'''
        return sum(ProductSeller.objects.filter(product=obj).values_list('quantity', flat=True))

    # Need to change this
    def get_feature(self, obj):
        '''Need to rewrite code'''
        feature_list = Feature.objects.filter(category=obj.category)
        features = {}
        for feature_object in feature_list:
            feature_name = feature_object.name
            feature_value = ProductFeature.objects.filter(
                feature=feature_object, product=obj).values_list('value', flat=True).get()
            features.update({feature_name: feature_value})
        return features

    def get_reviews(self, obj):
        '''fetch reviews'''
        return Review.objects.filter(product=obj).values('id',
                                                         'rating',
                                                         'user',
                                                         'title',
                                                         'description')


class WishlistSerializer(serializers.ModelSerializer):
    '''
    Wishlist Serializer
    '''
    class Meta:
        '''meta'''
        model = Wishlist
        fields = ('id', 'product')

    def create(self, validate_data):
        '''create'''
        return Wishlist.objects.create(user=self.context['request'].user, product=validate_data['product'])


class ProductSellerSerializer(serializers.ModelSerializer):
    '''
    Product Seller Serializer
    '''
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    selling_exprience = serializers.SerializerMethodField()
    delivery_days = serializers.SerializerMethodField()

    class Meta:
        '''meta'''
        model = ProductSeller
        fields = ('id',
                  'name',
                  'rating',
                  'selling_price',
                  'selling_exprience',
                  'delivery_days')

    def get_name(self, obj):
        '''Company Name'''
        return obj.seller.company_name

    def get_rating(self, obj):
        '''Rating'''
        return Review.objects.filter(seller=obj.seller).aggregate(Avg('rating'))['rating__avg']

    def get_selling_exprience(self, obj):
        '''selling experience'''
        return str(timezone.now().year - obj.created_at.year) + " years."

    def get_selling_price(self, obj):
        '''selling price'''
        price = obj.selling_price
        discount = obj.discount
        sp = price - (price * (discount / 100))
        return sp

    def get_delivery_days(self, obj):
        '''return delivery days'''
        return {"min": obj.min_delivery_days,
                "max": obj.max_delivery_days}


class ProductReviewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    '''
    Product Review Serializer
    '''
    class Meta:
        '''meta'''
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'title', 'description')


class SellerReviewSerializer(serializers.ModelSerializer):
    '''
    Seller Review Serializer
    '''
    class Meta:
        '''meta'''
        model = Review
        fields = ('id', 'user', 'seller', 'rating', 'title', 'description')
