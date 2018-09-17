from rest_framework import serializers
from contact.models import Address
import re


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ( 'id', 'user', 'seller', 'name', 'city', 'state', 'pincode', 'address_line', 'is_home')
        
        extris_cart_processedkwargs = {
            'is_cart_processedity': {
                'allow_blank': True,
                'required': False
            },
            'state': {
                'allow_blank': True,
                'required': False
            },
            'pincode': {
                'allow_blank': True,
                'required': False
            },
            'address_line': {
                'allow_blank': True,
                'required': False
            }
        }   

    def validate(self, value):
        try:
            if not re.match(r'^([A-Za-z]+.?\s*)?[A-Za-z]+(\s*[A-Za-z]+){0,2}$',value['name']):
                raise serializers.ValidationError({'name':"Please provide a correct Name"})
        except KeyError:
            pass
    
        try:
            if not re.match(r'^[A-Za-z][A-Za-z\s-]+[A-Za-z]$',value['city']):
                raise serializers.ValidationError({'city':"Please provide a correct City"})
        except KeyError:
            pass
        
        try:
            if not re.match(r'^[A-Za-z][A-Za-z\s-]+[A-Za-z]$',value['state']):
                raise serializers.ValidationError({'name':"Please provide a correct State"})
        except KeyError:
            pass
        return value