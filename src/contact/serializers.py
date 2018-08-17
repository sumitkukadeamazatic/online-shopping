from rest_framework import serializers
from contact.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ( 'id', 'user', 'seller', 'name', 'city', 'state', 'pincode', 'address_line', 'is_home')
        extra_kwargs = {
            'name': {
                'allow_blank': True,
                'required': False
            },
            'city': {
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