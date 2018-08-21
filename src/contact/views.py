"""
   Contact App Views
"""
from contact.models import Address
from rest_framework.authtoken.models import Token
from contact.serializers import AddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if (not auth or auth[0].lower() != 'token') or len(auth) != 2:
            return  {'Error': "Invalid token header. No credentials provided."}
        if auth[1]=="null":
            return {'Error': "Null token not allowed"}
        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, token):
        msg = {'Error': "Token mismatch"}
        try:
            user_id = Token.objects.get(key=token).user_id
        except:
            return {'Error': "Token matching query does not exist."}
        if not user_id:
            return msg
        return (user_id, token)


class AddressList(APIView):
    """
    Address Vies is use to Create, Update, Delete adresses
    """
    def get(self, request, format=None):
       
        tokenAuth = TokenAuthentication()
        res = tokenAuth.authenticate(request)
        if len(res)!=2:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        user_id , token = res

        address = None
        if request.GET.get('flag'):
            address = Address.objects.filter(user_id = user_id).order_by('id')
        else:
            address = Address.objects.filter(seller_id = request.GET.get('id')).order_by('id')
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        tokenAuth = TokenAuthentication()
        res = tokenAuth.authenticate(request)
        if len(res)!=2:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        user_id , token = res

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):

        tokenAuth = TokenAuthentication()
        res = tokenAuth.authenticate(request)
        if len(res)!=2:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        user_id , token = res
        
        address = Address.objects.get(pk=request.data['id'])
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):

        tokenAuth = TokenAuthentication()
        res = tokenAuth.authenticate(request)
        if len(res)!=2:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        user_id , token = res

        address = Address.objects.get(pk=request.data['id'])
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)