from rest_framework import serializers
from .models import Seller


class SellerSerializer(serializers.Serializer):
    message = serializers.CharField(max_length = 200)

    class Meta:
        model = Seller
        fields = (
            'id',
            'company_name',
            'contact_number'
        )
#        extra_kwargs = 

class SellerDetailSerializer(serializers.Serializer):
    seller_id = serializers.IntegerField()
    company_name = serializers.CharField(max_length=50)
    user_id = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    ''' review = 
        following fields tobe placed in array of JSON.
    '''
    user_name = serializers.CharField(max_length=50)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    review_date = serializers.DateTimeField()
