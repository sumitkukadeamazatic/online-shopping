from rest_framework import serializers
from .models import Seller
from product.models import Review
from django.db.models import Avg


class SellerSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField('get_msg')

    class Meta:
        model = Seller
        read_only_fields = ('message',)
        fields = (
            'id',
            'created_at',
            'updated_at',
            'company_name',
            'contact_number',
            'status',
            'message'
        )


    def get_msg(self, obj):
        return "Post Method"


class SellerDetailSerializer(serializers.ModelSerializer):

    #current_user = serializers.SerializerMethodField('getUser')
    average_rating = serializers.SerializerMethodField('getAverageRating')

    class Meta:
        model = Seller
        fields = (
            'id',
            'company_name',
            'average_rating'
        )

    def getAverageRating(self, obj):
        print (Seller.id)
        #print (Review.objects.filter(seller_id = 11))
        #print (Review.objects.filter(seller_id = id).aggregate(Avg('rating')))
        return (Review.objects.filter(seller_id = 11).aggregate(Avg('rating'))['rating__avg'])

'''
    def getUser(self, obj):
        request = getattr(self.context, 'request', None)
        print (request.user)
        #print (self.context['abc'])
        #print (serializers.CurrentUserDefault())
        #user_id = self.context.get("user_id")
        #print (user_id)
        #print (self.context['abc'])
        if user_id:
            return user_id
'''

'''
    seller_id = serializers.IntegerField()
    company_name = serializers.CharField(max_length=50)
    user_id = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    """ review = 
        following fields tobe placed in array of JSON.
    """
    user_name = serializers.CharField(max_length=50)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    review_date = serializers.DateTimeField()
'''
