"""
product app models
"""
from rest_framework.views import APIView
from rest_framework.response import Response
#from django.http import Http404
from rest_framework import permissions, authentication#, status
# from django.shortcuts import render

from django.core.paginator import Paginator
#from django.http import JsonResponse
#from .serializers import CategorySerializer
from .models import Category, Product, ProductSeller, Review

def add_peginator(results, requested_page_no, items_per_page):
    '''
    This function will return data with pagination
    it will take list of json and return filterd result
    with pagination of json type
    '''
    data = {}
    page = {}
    results_paginator = Paginator(results, items_per_page)
    page_paginator = results_paginator.get_page(requested_page_no)
    no_of_pages = results_paginator.num_pages


    page['current_page'] = requested_page_no if requested_page_no <= no_of_pages and requested_page_no > 0 else "Invalid page number"
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
        return Response(add_peginator(results, requested_page_no, 1))



class ProductView(APIView):
    """
    Product view
    """
    def get(self, request):
        pass
    def filter_product_list(self,
                            product_id,
                            category_id,
                            seller_id,
                            min_price,
                            max_price,
                            brand_list,
                            discount,
                            feature_slug,
                            rating):
        if seller_id != r'.*':
            if not ProductSeller.objects.filter(
                    product_id=product_id,
                    seller_id=seller_id).exists():
                return False

            if brand_list != r'.*':
                is_exists = False
                for brand_id in brand_list:
                    if Product.objects.values().filter(brand_id=brand_id).exists():
                        is_exists = True
                        break
                if not is_exists:
                    return False

        product_selling_price = Product.objects.values_list(
            'selling_price', flat=True).filter(id=product_id).get()
        if min_price != r'.*':
            if product_selling_price < min_price:
                return False
        if max_price != r'.*':
            if product_selling_price > max_price:
                return False

        total_ratings = list(Review.objects.values_list(
            'rating', flat=True).filter(product_id=product_id))

        if total_ratings < rating:
            return False

        price = Product.objects.values('base_price', 'selling_price').filter(id=product_id).get()
        product_discount = (price['base_price']-price['selling_price']) /price['base_price'] * 100
        if product_discount < float(discount):
            return False

        return True

    def post(self, request, format=None):
        category_slug = request.data.get('category_slug', r'.*')
        seller_id = request.data.get('seller_id', r'.*')
        rating = request.data.get('rating', r'.*')
        min_price = request.data.get('min_price', r'.*')
        max_price = request.data.get('max_price', r'.*')
        brand = request.data.get('brand', r'.*')
        discount = request.data.get('discount', r'.*')
        feature_slug = request.data.get('feature_slug', r'.*')
        rating = request.data.get('rating', r'.*')
        # Fetching category id from category slug
        category_id = list(Category.objects.values_list('id', flat=True).filter(
            slug=category_slug))
        category_id = category_id[0] if len(category_id) == 1 else None
        # product id list 
        #product_id_list = list(models.Product.objects.values_list("id",flat=True))
        product_id_list = list(Product.objects.values_list('id', flat=True).filter(
            category_id=category_id))
        
        filter_flag = True
        for pro_id in product_id_list:
            if category_slug == r'.*':
                pass
        # Fetching brand id from
        products = list(Product.objects.values(
            "brand",
            "category",
            "name",
            "description",
            "base_price",
            "selling_price",
            "slug",
            "images"
            ).filter())

        #print(products[0])


        return Response({"products":products})
