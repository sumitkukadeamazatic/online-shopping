from rest_framework import serializers
from .models import Seller, User
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

    class Meta:
        model = Seller
        fields = (
            'id',
            'company_name',
        )

class ReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField('get_userName')
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        
        fields = (
            'user_id',
            'user_name',
            'rating',
            'title',
            'description',
            'created_at'
        )

    def get_userName(self,obj):
        print(obj.rating)
        user_name_dic = User.objects.values('first_name','middle_name','last_name').filter(id=obj.user_id).first()
        user_name = ' '.join(filter(None,(map(lambda x:user_name_dic[x],user_name_dic))))
        return user_name

    #def to_representation(self,obj):
        #serialized_data = super(ReviewSerializer, self).to_representation(obj)
        #print (avg)
        #print (serialized_data)
        #a = [sum(float(serialized_data['rating'])) for serialized_data['rating'] in serialized_data]
        #print(a)
        #print (sum(float(serialized_data['rating'])))

'''
class SellerDetailSerializer(serializers.ModelSerializer):

    #current_user = serializers.SerializerMethodField('getUser')
    #average_rating = serializers.SerializerMethodField('getAverageRating')

    #seller_id = serializers.SerializerMethodField('getId')    
    #result = Seller.objects.filter(id=11)
#    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = (
            'id',
            'company_name',
#            'review'
#            'average_rating',
#            'review'
        )

    def getId(self, validated_data):
        print (validated_data.objects.filter(id=11))
        #print (validated_data.pop('id'))


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
