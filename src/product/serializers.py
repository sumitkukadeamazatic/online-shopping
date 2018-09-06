"""
    serializers for product app
"""
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer
from offer.models import Offer
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
        fields = ('id', 'product')


class WishlistPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product')


class OfferSerializer(ModelSerializer):
    """
       Serializer for product's offer listing.
    """

    product_slug = serializers.SlugField()

    class Meta:
        model = Offer
        fields = ('id', 'name', 'description', 'amount', 'percentage', 'amount_limit',
                  'minimum', 'valid_from', 'valid_upto', 'start_time', 'end_time', 'product_slug')
        extra_kwargs = {
            'product_slug': {
                'write_only': True
            },
            'name': {
                'required': False
            },
            'description': {
                'required': False
            }
        }

    def validate(self, data):
        """
            Validate product slug
        """
        print('in validate method')
        print(data)
        return data
