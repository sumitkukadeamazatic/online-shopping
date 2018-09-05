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
from .models import Category, Wishlist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import WishlistSerializer, WishlistPostSerializer


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
        requested_page_no = int(request.GET.get('page', False))
        requested_category_slug = request.GET.get('category_slug', None)
        items_per_page = 10
        parentid = [x.id for x in Category.objects.all().filter(
            slug=requested_category_slug)]
        print(parentid)
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
        results_paginator = Paginator(results, items_per_page)
        page_paginator = results_paginator.get_page(requested_page_no)
        no_of_pages = results_paginator.num_pages
        if not requested_page_no:
            results = results_paginator.object_list
        else:
            results = results_paginator.get_page(requested_page_no).object_list
        page = {}
        page['current_page'] = requested_page_no if requested_page_no < no_of_pages and requested_page_no > 0 else "Invalid page number"
        page['items_per_page'] = items_per_page
        page['no_of_pages'] = no_of_pages
        page['has_previous'] = page_paginator.has_previous()
        page['has_next'] = page_paginator.has_next()
        data = {}
        data['page'] = page
        data['results'] = page_paginator.object_list

        return Response(data)
