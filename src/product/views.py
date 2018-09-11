"""
product app models
"""
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication#, status
from rest_framework import viewsets
from django.http import Http404#, JsonResponse
# from django.shortcuts import render

from django.core.paginator import Paginator
#from .serializers import CategorySerializer
from .models import Category, Product, ProductSeller, Review, ProductFeature, Feature, User
from seller.models import Seller, SellerUser
from .models import Category, Wishlist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import (WishlistSerializer,
                          WishlistPostSerializer,
                          CategorySerializer,
                          ProductSerializer)


class WishlistViewset(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        queryset = Wishlist.objects.filter(user=user)
        serializer = WishlistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = {}
        data['product'] = request.data['product']
        data['user'] = self.request.user.id
        serializer = WishlistPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        res = Wishlist.objects.get(pk=pk,user=self.request.user.id).delete()
        return Response({"Msage":"deleted  sussesfully"},status=status.HTTP_204_NO_CONTENT)

class CategoryView(viewsets.ModelViewSet):
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk=None):
        par_id = Category.objects.values_list('id', flat=True).filter(slug=pk)
        par_id = par_id[0] if len(par_id) == 1 else None
        categories = Category.objects.filter(parent_id=par_id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
 


class ProductSellerView(APIView):
    def get(self, request):
        data = {}
        product_slug = request.GET.get('product_slug', None)
        product_id = list(Product.objects.values_list(
            'id', flat=True).filter(slug=product_slug))
        product_id = product_id[0] if len(product_id) == 1 else None
        seller_list = list(ProductSeller.objects.values_list(
            'seller_id', flat=True).filter(product_id=product_id))
        product_detail = Product.objects.values().filter(id=product_id)
        if product_detail:
            product_detail = product_detail[0]
        else:
            return Response({"response":"Invalid request."})
        seller_details = []
        for sid in seller_list:
            sd = Seller.objects.values().filter(id=sid).get()
            # seller and product relation
            spd = list(ProductSeller.objects.filter(
                seller_id=sid, product_id=product_id).values())
            spd = spd[0] if spd else None
            seller_detail = {}
            seller_detail['id'] = sid
            seller_detail['name'] = sd['company_name']
            ratings = Review.objects.values_list('rating', flat=True).filter(seller_id=sid)
            try:
                ratings = sum(ratings)/len(ratings)
            except ZeroDivisionError:
                ratings = "Ratings not available."

            seller_detail['rating'] = ratings
            base_price = float(product_detail['base_price'])
            discount = float(spd['discount'])
            seller_detail['selling_price'] = base_price-(base_price*discount/100)
            experience = datetime.datetime.now().year - sd['created_at'].year
            seller_detail["selling_exprience"] = str(experience) + " year(s)."
            seller_detail['delivery_days'] = {"min" : spd['min_delivery_days'],
                                              "max" : spd['max_delivery_days']}
            seller_details.append(seller_detail)


        data['sellers'] = seller_details
        return Response(data)

class ReviewView(APIView):
    def get(self, request, format=None):
        resp = {}
        seller_id = request.GET.get('seller_id', False)
        product_id = request.GET.get('product_id', False)

        if not (bool(seller_id) ^ bool(product_id)):
            return Response({"response":"Invalid Request."})

        if seller_id:
            reviews = list(Review.objects.filter(seller_id=seller_id).values('id',
                                                                             'title',
                                                                             'seller_id',
                                                                             'user_id',
                                                                             'created_at',
                                                                             'updated_at',
                                                                             'description',
                                                                             'rating'))
        if product_id:
            reviews = list(Review.objects.filter(product_id=product_id).values('id',
                                                                               'title',
                                                                               'product_id',
                                                                               'user_id',
                                                                               'created_at',
                                                                               'updated_at',
                                                                               'description',
                                                                               'rating'))

        for review in reviews:
            user_id = review.pop('user_id')
            try:
                review["user_name"] = User.objects.filter(id=user_id).values('first_name',
                                                                             'middle_name',
                                                                             'last_name').get()
            except Exception:
                review["user_name"] = "Not available."

        resp["reviews"] = reviews


        #return Response(resp)
        #product_id = request.data.get("product_id", None)
        #seller_id = request.data.get("seller_id", None)
        #rating = request.data.get("rating", None)
        #title = request.data.get("title", None)
        #description = request.data.get("description", None)
        return Response(resp)

    def post(self, request, format=None):
        data = {}
        data['product_id'] = request.data.get('product_id', False)
        data['seller_id'] = request.data.get('seller_id', False)
        data['rating'] = request.data.get('rating', False)
        data['title'] = request.data.get('title', False)
        data['description'] = request.data.get('description', False)

        if not (bool(data['seller_id']) ^ bool(data['product_id'])):
            return Response({"status":"Invalid Request."})

        return Response(data)



