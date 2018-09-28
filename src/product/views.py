"""
product app models
"""
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, ProductSeller, Review, ProductFeature, Feature, User, Wishlist
from seller.models import Seller, SellerUser
from rest_framework import viewsets, status
from rest_framework.response import Response

from .filters import ProductFilter
from .serializers import (WishlistSerializer,
                          CategorySerializer,
                          ProductReviewSerializer,
                          SellerReviewSerializer,
                          ProductSellerSerializer,
                          ProductSerializer)


class WishlistViewset(viewsets.ModelViewSet):
    '''
    Wishlist view -
    to get wishlisted product of logged in user
    only logged in user can access view
    '''
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class CategoryView(viewsets.ReadOnlyModelViewSet):
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class ProductView(viewsets.ReadOnlyModelViewSet):
    '''
    Product View: 
    to get product list also added filters
    '''
    queryset = Product.objects.all()
    filter_class = ProductFilter
    filter_fields = ('slug')
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

class ProductSellerView(viewsets.ModelViewSet):
    '''
    Product Seller view -
    to get product seller of product
    anyone can access view
    '''
    queryset = ProductSeller.objects.all()
    lookup_field = 'product'
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSellerSerializer


class SellerReviewView(viewsets.ModelViewSet):
    '''
    Seller view -
    to get seller reviews
    anyone can access view
    '''
    queryset = Review.objects.all()
    lookup_field = 'seller_id'
    permission_classes = (permissions.AllowAny,)
    serializer_class = SellerReviewSerializer


class ProductReviewView(viewsets.ModelViewSet):
    '''
    Product view -
    to get product reviews
    anyone can access view
    '''
    queryset = Review.objects.all()
    lookup_field = 'product_id'
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductReviewSerializer
