"""
    this file is used to filter the products
"""
#'''Product Filter'''
import django_filters
from django_filters import rest_framework as filters
from .models import Product
class ProductFilter(filters.FilterSet):
    """
        this filter class is used to filter the product
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name="base_price", lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr='lte')
    #rating = django_filters.NumberFilter(field_name='Review', lookup_expr='gte')
    class Meta:
        model = Product
        fields = ['name', 'slug', 'min_price', 'max_price', 'category']
