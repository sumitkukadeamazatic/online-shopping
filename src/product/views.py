"""
product app models
"""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from .models import Category, Product, ProductSeller, Review, Wishlist
from .filters import ProductFilter
from .permissions import UserAccessPermission, _user_access
from .serializers import (WishlistSerializer,
                          CategorySerializer,
                          ProductReviewSerializer,
                          SellerReviewSerializer,
                          ProductSellerSerializer,
                          ProductSerializer)


class WishlistViewset(ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    Wishlist view -
    to get wishlisted product of logged in user
    only logged in user can access view
    '''
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class CategoryView(ReadOnlyModelViewSet): # pylint: disable=too-many-ancestors
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductView(ReadOnlyModelViewSet): # pylint: disable=too-many-ancestors
    '''
    Product View:
    to get product list also added filters
    '''
    queryset = Product.objects.all()
    filter_class = ProductFilter
    filter_fields = ('slug')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductSellerView(ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    Product Seller view -
    to get product seller of product
    anyone can access view
    '''
    queryset = ProductSeller.objects.all()
    lookup_field = 'product'
    permission_classes = [AllowAny]
    serializer_class = ProductSellerSerializer


class SellerReviewView(ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    Seller view -
    to get seller reviews
    anyone can access view
    '''
    queryset = Review.objects.exclude(seller__isnull=True)
    lookup_field = 'seller'
    serializer_class = SellerReviewSerializer
    def get_permissions(self):
        return _user_access(self.action)

class ProductReviewView(ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    Product view -
    to get product reviews
    anyone can access view
    '''
    queryset = Review.objects.exclude(product__isnull=True)
    lookup_field = 'product'
    serializer_class = ProductReviewSerializer
    def get_permissions(self):
        return _user_access(self.action)
