"""
    This serializer is used to Address API
"""
import re
from rest_framework import serializers
from contact.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
        This class used in Address API
    """
    class Meta:
        model = Address
        fields = ('id', 'user', 'seller', 'name', 'city', 'state', 'pincode', 'address_line', 'is_home', 'contact_no')

        extra_kwargs = {
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
    def validate_name(self, value): #pylint: disable=no-self-use
        """
            this method is used to validate name
        """
        if not re.match(r'^([A-Za-z]+.?\s*)?[A-Za-z]+(\s*[A-Za-z]+){0,2}$', value):
            raise serializers.ValidationError({'name':"Please provide a correct Name"})
        return value

    def validate_city(self, value): #pylint: disable=no-self-use
        """
            this method is used to validate city
        """
        if not re.match(r'^([A-Za-z]+.?\s*)?[A-Za-z]+(\s*[A-Za-z]+){0,2}$', value):
            raise serializers.ValidationError({'city':"Please provide a correct city"})
        return value

    def validate_state(self, value): #pylint: disable=no-self-use
        """
            this method is used to validate state
        """
        if not re.match(r'^([A-Za-z]+.?\s*)?[A-Za-z]+(\s*[A-Za-z]+){0,2}$', value):
            raise serializers.ValidationError({'state':"Please provide a correct state"})
        return value
