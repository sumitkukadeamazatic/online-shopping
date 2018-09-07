from rest_framework import serializers
from .models import Seller, User
from product.models import Review
from django.db.models import Avg
from rest_framework.validators import ValidationError


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = (
            'id',
            'created_at',
            'updated_at',
            'company_name',
            'contact_number',
            'status',
        )

    def validate(self, obj):
        if not obj['contact_number'].isdigit():
            raise ValidationError({'contact_number': 'Contact number must contain number'})
        return obj


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

    def get_userName(self, obj):
        user_name_dic = User.objects.values('first_name','middle_name','last_name').filter(id=obj.user_id).first()
        user_name = ' '.join(filter(None,(map(lambda x:user_name_dic[x],user_name_dic))))
        return user_name

    #def to_representation(self,obj):
        #serialized_data = super(ReviewSerializer, self).to_representation(obj)
        #print (serialized_data)

