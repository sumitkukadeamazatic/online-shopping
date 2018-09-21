#'''Product Filter'''
#from django_filters import FilterSet, CharFilter, NumberFilter
#from .models import Product

#class ProductFilter(FilterSet):
    #name = CharFilter(name='name', lookup_type='exact', distinct=True)
    #class Meta:
        #model = Product
        #fields = ['name']

import django_filters
from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    slug = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Product
        fields = ['name','slug']
