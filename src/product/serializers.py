"""
    serializers for product app
"""
from django.utils import timezone
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueTogetherValidator
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
    sub_category = serializers.SerializerMethodField()
    class Meta:
        '''meta'''
        model = Category
        fields = ('id', 'name', 'slug', 'sub_category')
    def get_sub_category(self, obj): #pylint: disable=no-self-use
        '''Getting subcategory'''
        return Category.objects.filter(parent=obj.id).values('id', 'name', 'slug')

class ProductFeatureSerializer(serializers.ModelSerializer):
    '''get product feature'''
    class Meta:
        '''meta'''
        model = ProductFeature
        fields = ('feature', 'value')

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

    def get_rating(self, obj): #pylint: disable=no-self-use
        '''rating'''
        return Review.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']

    def get_in_stock(self, obj): #pylint: disable=no-self-use
        '''check all stock from all seller'''
        return sum(ProductSeller.objects.filter(product=obj).values_list('quantity', flat=True))

    # Need to change this
    def get_feature(self, obj): #pylint: disable=no-self-use
        '''Need to rewrite code'''
        feature_list = Feature.objects.filter(category=obj.category)
        #return ProductFeatureSerializer(feature_list)
        features = {}
        for feature_object in feature_list:
            feature_name = feature_object.name
            feature_value = ProductFeature.objects.filter(
                feature=feature_object, product=obj).values('value')
            if not feature_value:
                feature_value = None
            features.update({feature_name: feature_value})
        return features

    def get_reviews(self, obj): #pylint: disable=no-self-use
        '''fetch reviews'''
        return Review.objects.filter(product=obj).values('id',
                                                         'rating',
                                                         'user',
                                                         'title',
                                                         'description')[:3]

class ProductListingSerializer(serializers.ModelSerializer):

    class Meta:
        '''meta'''
        model = Product
        fields = ('name', 'description', 'images', 'base_price', 'brand', 'slug', 'category')
    
    def validate_category(self, value):
        # Seller can only add product in sub-category only
        if not Category.objects.filter(name=value, parent__isnull=False):
            raise serializers.ValidationError("Product Listing is allowd only in sub-categories only.")
        return value

class WishlistSerializer(serializers.ModelSerializer):
    '''
    Wishlist Serializer
    '''
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    class Meta:
        '''meta'''
        model = Wishlist
        fields = ('id', 'product_seller','name','rating','selling_price')

    def create(self, validate_data): #pylint: disable=arguments-differ
        '''create'''
        if Wishlist.objects.filter(product_seller=validate_data['product_seller']):
            raise ParseError(detail='product already exist in wishlist')
        return (Wishlist.objects.create(user=self.context['request'].user,
                                        product_seller=validate_data['product_seller']))

    def get_name(self, obj): #pylint: disable=no-self-use
        '''Product Name'''
        return obj.product_seller.product.name

    def get_rating(self, obj): #pylint: disable=no-self-use
        '''Rating'''
        return Review.objects.filter(
            product=obj.product_seller.product).aggregate(Avg('rating'))['rating__avg']

    def get_selling_price(self, obj): #pylint: disable=no-self-use
        '''selling price'''
        price = obj.product_seller.selling_price
        discount = obj.product_seller.discount
        selling_price = price - (price * (discount / 100))
        return selling_price


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
                  'product',
                  'delivery_days',
                  'is_default')

    def get_name(self, obj): #pylint: disable=no-self-use
        '''Company Name'''
        return obj.seller.company_name

    def get_rating(self, obj): #pylint: disable=no-self-use
        '''Rating'''
        return Review.objects.filter(seller=obj.seller).aggregate(Avg('rating'))['rating__avg']

    def get_selling_exprience(self, obj): #pylint: disable=no-self-use
        '''selling experience'''
        return str(timezone.now().year - obj.created_at.year) + " years."

    def get_selling_price(self, obj): #pylint: disable=no-self-use
        '''selling price'''
        price = obj.selling_price
        discount = obj.discount
        selling_price = price - (price * (discount / 100))
        return selling_price

    def get_delivery_days(self, obj): #pylint: disable=no-self-use
        '''return delivery days'''
        return {"min": obj.min_delivery_days,
                "max": obj.max_delivery_days}


class ProductReviewSerializer(serializers.ModelSerializer):
    '''ProductReviewSerializer'''
    class Meta:
        '''meta'''
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'title', 'description')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.exclude(product__isnull=True), fields=('user', 'product'), )]


class SellerReviewSerializer(serializers.ModelSerializer):
    '''
    Seller Review Serializer
    '''
    class Meta:
        '''meta'''
        model = Review
        fields = ('id', 'user', 'seller', 'rating', 'title', 'description')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.exclude(seller__isnull=True), fields=('user', 'seller'), )]
