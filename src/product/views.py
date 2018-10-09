"""
product app models
"""
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        IsAdminUser)
from .filters import ProductFilter
from .models import Category, Product, ProductSeller, Review, Wishlist
from .serializers import (WishlistSerializer,
                          CategorySerializer,
                          ProductReviewSerializer,
                          SellerReviewSerializer,
                          ProductSellerSerializer,
                          ProductSerializer)


class WishlistViewset(viewsets.ModelViewSet): #pylint: disable=too-many-ancestors
    '''
    Wishlist view -
    to get wishlisted product of logged in user
    only logged in user can access view
    '''
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthenticated,)
    serializer_class = WishlistSerializer

    def get_queryset(self):
        """
            tihs method is used to filter whishlist queryset using user
        """
        return Wishlist.objects.filter(user=self.request.user)


class CategoryView(viewsets.ReadOnlyModelViewSet): #pylint: disable=too-many-ancestors
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.exclude(parent__isnull=False)
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

class ProductView(viewsets.ReadOnlyModelViewSet): #pylint: disable=too-many-ancestors
    '''
    Product View:
    to get product list also added filters
    '''
    queryset = Product.objects.all()
    filter_class = ProductFilter
    filter_fields = ('slug')
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

class ProductSellerView(viewsets.ModelViewSet): #pylint: disable=too-many-ancestors
    '''
    Product Seller view -
    to get seller list of selling given product
    anyone can access to retrive
    '''
    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAdminUser,)
        return super(ProductSellerView, self).get_permissions()

    def retrieve(self, request, pk=None):
        queryset = ProductSeller.objects.all()
        seller = get_list_or_404(queryset, product=pk)
        serializer = ProductSellerSerializer(seller, many=True)
        page = self.paginate_queryset(self.queryset)
        return self.get_paginated_response(serializer.data)


    queryset = ProductSeller.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSellerSerializer


class SellerReviewView(viewsets.ModelViewSet): #pylint: disable=too-many-ancestors
    '''
    Seller view -
    to get seller reviews
    anyone can access view
    '''
    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super(SellerReviewView, self).get_permissions()


    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        review = get_list_or_404(queryset, seller=pk)
        serializer = SellerReviewSerializer(review, many=True)
        #return Response(serializer.data)
        page = self.paginate_queryset(self.queryset)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        '''Overriding create, to add logged in user id'''
        request.data['user'] = request.user.id
        return super().create(request)

    queryset = Review.objects.exclude(seller__isnull=True)
    serializer_class = SellerReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



class ProductReviewView(viewsets.ModelViewSet): #pylint: disable=too-many-ancestors
    '''
    Product view -
    to get product reviews
    anyone can access view
    '''

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (IsAdminUser,)
        else:
            self.permission_classes = (IsAuthenticatedOrReadOnly,)
        return super(ProductReviewView, self).get_permissions()


    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        review = get_list_or_404(queryset, product=pk)
        serializer = ProductReviewSerializer(review, many=True)
        page = self.paginate_queryset(self.queryset)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        '''Overriding create, to add logged in user id'''
        request.data['user'] = request.user.id
        return super().create(request)

    queryset = Review.objects.exclude(product__isnull=True)
    serializer_class = ProductReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
