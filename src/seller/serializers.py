from rest_framework import serializers


class SellerSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50, required=True)


class SellerDetailSerializer(serializers.Serializer):
    seller_id = serializers.BigIntegerField()
    company_name = serializers.CharField(max_length=50)
    user_id = serializers.BigIntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_place=2)
    ''' review = 
        following fields tobe placed in array of JSON.
    '''
    user_name = serializers.CharField(max_length=50)
    rating = serializers.DecimalField(max_digits=3, decimal_place=2)
    title = serializers.CharField(max_length=50)
    description = serializers.TextField()
    review_date = serializers.DateTimeField()
