"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import UserAccessPermission

class AddressViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        try:
            user = self.request.user
            return Address.objects.filter(user=user)
        except TypeError:
            return Response({'Error':'Add Token To request Heder'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        

    serializer_class = AddressSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]


    def get_paginated_response(self, data):
       return Response(data)