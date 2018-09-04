"""
    serializers for product app
"""
from rest_framework import serializers, exceptions
from .models import Category, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    """
        serializers for product app
    """
    name = serializers.CharField(read_only=True)
    token = serializers.SerializerMethodField('generate_token')
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        '''meta'''
        model = 'Category'
        #fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id','product')

class WishlistPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id','user','product')
