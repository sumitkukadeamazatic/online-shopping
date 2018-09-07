"""
     Seller App Views
"""

# from django.shortcuts import render
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import SellerUser, Seller, User
from product.models import Review


class SellerView(APIView):

    def get(self, request, format=None):
        seller_id = request.GET['seller_id']
        seller_result = Seller.objects.get(id=seller_id)
        review_result = Review.objects.filter(seller=seller_id)
        seller_response = SellerDetailSerializer(seller_result)
        review_response = ReviewSerializer(review_result, many=True)
        average_rating = Review.objects.filter(seller_id=seller_id).aggregate(Avg('rating'))['rating__avg']
        average_rating = '%.2f' % (0 if average_rating is None else average_rating)
        updated_seller_data = {'average_rating': average_rating}
        updated_seller_data.update(seller_response.data)
        updated_review_data = {'review': review_response.data}
        updated_review_data.update(updated_seller_data)
        return Response(updated_review_data)

    def post(self, request, format=None):
        sellerResponse = SellerSerializer(data=request.data)
        # print (repr(sellerResponse))
        if sellerResponse.is_valid():
            sellerResponse.save()
            # sellerId = Seller.objects.get(id=sellerResponse.data['id'])
            # userId = User.objects.get(id=request.user.id)
            # SellerUser(seller=sellerId,user=userId).save()
            SellerUser(seller_id=sellerResponse.data['id'], user_id=request.user.id).save()
            # return Response({'token': request.META.get('HTTP_AUTHORIZATION')}, status=status.HTTP_201_CREATED)
            return Response({'token': str(Token.objects.get(user_id=request.user.id))}, status=status.HTTP_201_CREATED)
        return Response(sellerResponse.errors, status=status.HTTP_400_BAD_REQUEST)


'''
        print (request.META.get('HTTP_TOKEN'))
        print (Token.objects.get(key=request.META.get('HTTP_TOKEN')).user.id)
        #return JsonResponse(serializer.data)
        #request.POST = request.POST.copy()
        #request.POST.update({'message':'Post Method'})

class SellerViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self,request):
        print(request.data)
        data = {'message':'list method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)

    def create(self, request):
        print (request.data)
        data = {'message':'create method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)
'''
