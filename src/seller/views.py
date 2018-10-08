"""
     Seller App Views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import SellerUser, Seller, User
from product.models import Review
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class SellerView(APIView):
    """
        Seller View using class based views
    """

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


class SellerViewSet(viewsets.ModelViewSet):
    """
        Seller View using Model Viewset
    """

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    #permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        print (self.action)
        print (self.request.user.is_superuser)
        if self.action == 'retrieve':
            return SellerDetailSerializer
        else:
            return SellerSerializer
