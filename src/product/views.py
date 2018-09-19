"""
product app models
"""
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status

from .models import Category, Product, ProductSeller, Review, ProductFeature, Feature, User
from seller.models import Seller, SellerUser
from .models import Wishlist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import UserAccessPermission
from .serializers import (WishlistSerializer,
                          WishlistPostSerializer,
                          ReviewPostSerializer,
                          CategorySerializer,
                          ReviewSerializer,
                          ProductSellerSerializer,
                          ProductSerializer)

class WishlistViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]
    serializer_class = WishlistSerializer

    def get_paginated_response(self, data):
        return Response(data)

class CategoryView(viewsets.ModelViewSet):
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductView(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(queryset, many=True)
        permission_classes = (permissions.AllowAny,)
        return Response(serializer_class.data)

    def create(self, request):
        data = request.data
        queryset = Product.objects.filter(brand__in=data['brand'],
                                          category__in=data["category_id"],
                                          base_price__gte=data["min_price"],
                                          base_price__lte=data["max_price"])
        pro_id = queryset.values_list('id', flat=True)
        exclude_list = []
        for pid in pro_id:
            pro_ratings = Review.objects.filter(product=pid).values_list('rating', flat=True)
            if pro_ratings:
                if (sum(pro_ratings)/len(pro_ratings)) < data["rating"]:
                    exclude_list.append(pid)
            else:
                    exclude_list.append(pid)
            price = Product.objects.values('base_price',
                                           'selling_price').filter(id=pid).get()
            pro_discount = (price['base_price']-price['selling_price']) /price['base_price'] * 100
            if pro_discount < data["discount"]:
                if pid not in exclude_list:
                    exclude_list.append(pid)
        queryset = queryset.exclude(id__in=exclude_list)
        serializer_class = ProductSerializer(queryset, many=True)
        permission_classes = (permissions.AllowAny,)
        return Response(serializer_class.data)

class ProductSellerView(viewsets.ModelViewSet):
    def retrieve(self, request, pk=None):
        queryset = ProductSeller.objects.filter(product=pk)
        serializer_class = ProductSellerSerializer(queryset, many=True)
        return Response(serializer_class.data)

class ReviewView(viewsets.ModelViewSet):
    def list(self, request):
        seller_id = request.GET.get('seller_id', False)
        product_id = request.GET.get('product_id', False)
        # if seller_id and product_id is not given or both given
        if not (bool(seller_id) ^ bool(product_id)):
            return Response({"response":"Invalid Request."})

        if seller_id:
            queryset = Review.objects.filter(seller=seller_id)
        if product_id:
            queryset = Review.objects.filter(product=product_id)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['user'] = request.user.id
        try:
            if not (bool(data['seller']) ^ bool(data['product'])):
                return Response({"response":"Invalid Request."})
        except KeyError:
            return Response({"response":"Mandatory field(s) missing."})

        serializer = ReviewPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({})

    def partial_update(self, request, pk=None):
        data = request.data
        data['user'] = request.user.id
        try:
            if not (bool(data['seller']) ^ bool(data['product'])):
                return Response({"response":"Invalid Request."})
        except KeyError:
            return Response({"response":"Mandatory field(s) missing."})
        
        serializer = ReviewPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
