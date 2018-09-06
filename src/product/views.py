"""
product app models
"""
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication#, status
from django.http import Http404#, JsonResponse
# from django.shortcuts import render

from django.core.paginator import Paginator
#from .serializers import CategorySerializer
from .models import Category, Product, ProductSeller, Review, ProductFeature, Feature, User
from seller.models import Seller, SellerUser

def add_peginator(results, requested_page_no, items_per_page):
    '''
    This function will return data with pagination
    it will take list of json and return filterd result
    with pagination of json type
    '''
    data = {}
    page = {}
    try:
        requested_page_no = int(requested_page_no)
    except ValueError:
        requested_page_no = 1
    requested_page_no = requested_page_no if requested_page_no is not 0 else 5
    results_paginator = Paginator(results, items_per_page)
    page_paginator = results_paginator.get_page(requested_page_no)
    no_of_pages = results_paginator.num_pages

    in_range = requested_page_no in range(1, no_of_pages+1)
    page['current_page'] = requested_page_no if in_range else "Invalid page number"
    page['items_per_page'] = items_per_page
    page['no_of_pages'] = no_of_pages
    page['has_previous'] = page_paginator.has_previous()
    page['has_next'] = page_paginator.has_next()
    data['page'] = page

    if not requested_page_no:
        data['results'] = results_paginator.object_list
    else:
        data['results'] = page_paginator.object_list

    return data


class CategoryView(APIView):
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    authentication_classes = (authentication.TokenAuthentication,)
    #serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        """
        GET all category from db
        """
        try:
            requested_page_no = int(request.GET.get('page', False))
        except ValueError:
            requested_page_no = False
        requested_category_slug = request.GET.get('category_slug', None)
        items_per_page = 10
        parentid = list(Category.objects.values_list('id', flat=True).filter(
            slug=requested_category_slug))
        parentid = parentid[0] if len(parentid) == 1 else None

        if not requested_category_slug:
            results = list(Category.objects.values('id',
                                                   'name',
                                                   'slug'
                                                   ).filter(parent_id=requested_category_slug))
            for ele in results:
                ele['category'] = list(Category.objects.values('id',
                                                               'name',
                                                               'slug'
                                                              ).filter(parent_id=ele['id']))
        elif not parentid:
            results = []
        else:
            results = list(Category.objects.values('id',
                                                   'name',
                                                   'slug').filter(parent_id=parentid))
        return Response(add_peginator(results, requested_page_no, items_per_page))



class ProductView(APIView):
    """
    Product view
    """

    def filter_product_list(self, product_id, data_json):
        '''return false if any of the thing will not match'''
        if data_json['seller_ids']:
            is_exists = False
            for seller_id in data_json['seller_ids']:
                if ProductSeller.objects.filter(
                        product_id=product_id,
                        seller_id=seller_id).exists():
                    is_exists = True
                    break
            if not is_exists and data_json['seller_ids'] != []:
                return False

        if data_json['brands']:
            is_exists = False
            for brand_id in data_json['brands']:
                if Product.objects.values().filter(id=product_id, brand_id=brand_id).exists():
                    is_exists = True
                    break
            if not is_exists and data_json['brands'] != []:
                return False

        product_selling_price = Product.objects.values_list(
            'selling_price', flat=True).filter(id=product_id).get()
        if data_json['min_price']:
            if product_selling_price < data_json['min_price']:
                return False
        if data_json['max_price']:
            if product_selling_price > data_json['max_price']:
                return False

        total_ratings = list(Review.objects.values_list(
            'rating', flat=True).filter(product_id=product_id))
        try:
            average_rating = sum(total_ratings)/len(total_ratings)
            ## handled error if user sent value other than decimal/float/int.
            try:
                if average_rating < data_json['rating']:
                    return False
            except TypeError:
                pass
        except ZeroDivisionError:
            pass


        price = Product.objects.values('base_price', 'selling_price').filter(id=product_id).get()
        product_discount = (price['base_price']-price['selling_price']) /price['base_price'] * 100
        try:
            if product_discount < float(data_json['discount']):
                return False
        except ValueError:
            pass

        return True

    def get(self, request, id):
        '''
        Get product detail using id
        '''
        try:
            pro_details = Product.objects.values().filter(id=int(id)).get()
        except Exception as e:
            raise Http404("Product doesn't exist")
            #return Response({"response" : "Product not found"})
        response = {}
        response['name'] = pro_details['name']

        total_ratings = list(Review.objects.values_list(
            'rating', flat=True).filter(product_id=id))
        try:
            response['average_rating'] = sum(total_ratings)/len(total_ratings)
        except ZeroDivisionError:
            response['average_rating'] = 'Not available'

        response['base_price'] = pro_details['base_price']
        response['selling_price'] = pro_details['selling_price']
        response['img'] = pro_details['images']
        response['description'] = pro_details['description']
        feature_list = list(ProductFeature.objects.filter(product_id=id).values(
            'value', 'feature_id'))
        for feature in feature_list:
            feature.update(Feature.objects.filter(id=feature['feature_id']).values('name').get())
            feature.pop('feature_id')
        response['feature'] = feature_list
        response['in_stock'] = sum(list(ProductSeller.objects.filter(product_id=id).values_list(
            'quantity', flat=True)))

        ## fetching reviews
        reviews = list(Review.objects.values().filter(product_id=1))
        for review in reviews:
            username = ""
            full_name = list(User.objects.values_list(
                'first_name', 'middle_name', 'last_name').filter(id=1).get())
            for name in full_name:
                if name:
                    username += name + " "
            review.update({'username': username})
            review.pop('seller_id')
            print(review['username'])
        response['reviews'] = reviews



        return Response(response)

    def post(self, request, format=None):
        data_json = {}
        data_json['category_slug'] = request.data.get('category_slug', None)
        data_json['page_no'] = request.data.get('page_no', 1)
        data_json['items_per_page'] = request.data.get('items_per_page', 5)
        
        ## if category list is not sent then returning all products available in database
        if not data_json['category_slug']:
            products = list(Product.objects.values())
            return Response({"products":products})

        data_json['seller_ids'] = request.data.get('seller_id', [])
        data_json['rating'] = request.data.get('rating', 0.1)
        data_json['min_price'] = request.data.get('min_price', None)
        data_json['max_price'] = request.data.get('max_price', None)
        data_json['brands'] = request.data.get('brand', None)
        data_json['discount'] = request.data.get('discount', 0.0)
        data_json['feature_slug'] = request.data.get('feature_slug', None)
        # Fetching category id from category slug
        category_id = list(Category.objects.values_list('id', flat=True).filter(
            slug=data_json['category_slug']))
        data_json['category_id'] = category_id[0] if len(category_id) == 1 else None
        product_id_list = list(Product.objects.values_list('id', flat=True).filter(
            category_id=data_json['category_id']))
        products = []
        for pro_id in product_id_list:
            if self.filter_product_list(pro_id, data_json):
                products = products + list(Product.objects.filter(id=pro_id).values())

        products = add_peginator(products, data_json['page_no'], data_json['items_per_page'])


        return Response({"products":products})


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
