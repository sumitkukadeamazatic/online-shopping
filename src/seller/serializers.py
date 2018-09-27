from rest_framework import serializers
from .models import Seller, User, SellerUser
from product.models import Review
from django.db.models import Avg
from rest_framework.validators import ValidationError
from rest_framework.decorators import action

class SellerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerUser
        fields = (
            'seller',
            'user'
        )

class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = (
            'company_name',
            'contact_number',
            'status',
        )

    def validate_contact_number(self, value):
        print (value)
        if not value.isdigit():
            raise ValidationError({'contact_number': 'Contact number must contain number'})
        return value

    def create(self, obj):
        print (self.context['request'].user.id)
        request_data = self.context['request'].data
        seller_obj = Seller.objects.create(company_name=request_data['company_name'], contact_number=request_data['contact_number'], status=request_data['status'])
        seller_user_data = {'seller': seller_obj.id, 'user':self.context['request'].user.id}
        seller_user_serializer = SellerUserSerializer(data=seller_user_data)
        if seller_user_serializer.is_valid():
            seller_user_serializer.save()
        return seller_obj


class ReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review     
        fields = (
            'user_name',
            'rating',
            'title',
            'description',
            'created_at'
        )

    def get_user_name(self, obj):
        user_name_dic = User.objects.values('first_name','middle_name','last_name').filter(id=obj['user_id']).first()
        user_name = ' '.join(filter(None,(map(lambda x:user_name_dic[x],user_name_dic))))
        return user_name

    #def to_representation(self,obj):
        #serialized_data = super(ReviewSerializer, self).to_representation(obj)
        #print (serialized_data)

class SellerDetailSerializer(serializers.ModelSerializer):
    
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = (
            'id',
            'company_name',
            'average_rating',
            'reviews',
        )

    def get_average_rating(self, obj):
        avg_rating = Review.objects.filter(seller_id=obj.id).aggregate(Avg('rating'))['rating__avg']
        return '%.2f' % (0 if avg_rating is None else avg_rating)

    def get_reviews(self, obj):
        serializer_data = Review.objects.filter(seller=obj).values()
        return ReviewSerializer(serializer_data, many=True).data
