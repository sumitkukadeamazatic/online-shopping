"""
    serializers for product app
"""
from rest_framework import serializers, exceptions
from .models import Category


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
