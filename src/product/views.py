"""
product app models
"""
from rest_framework.views import APIView
#from rest_framework.response import Response
#from django.http import Http404
from rest_framework import permissions#, status
# from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import JsonResponse
from .serializers import *
from .models import *

class CategoryView(APIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        data = {}
        requested_page_no = request.GET.get('page', False)
        requested_category_slug = request.GET.get('category_slug', False)
        items_per_page = 10

        results = list(Category.objects.values('id', 'name', 'slug').filter(parent_id=None))
        results_paginator = Paginator(results, items_per_page)
        page_paginator = results_paginator.get_page(int(requested_page_no))

        #no_of_pages = -(-(len(results))//items_per_page)
        no_of_pages = results_paginator.num_pages

        page = {}
        page['current_page'] = int(requested_page_no)
        page['items_per_page'] = items_per_page
        page['no_of_pages'] = no_of_pages
        page['has_previous'] = page_paginator.has_previous()
        page['has_next'] = page_paginator.has_next()

        if not requested_category_slug and not requested_page_no:
            data['results'] = results
            return JsonResponse(data)

        data['page'] = page

        data['results'] = page_paginator.object_list

        return JsonResponse(data)
