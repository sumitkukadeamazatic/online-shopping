from rest_framework import serializers, exceptions
from .models import User
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)
    token = serializers.SerializerMethodField('generate_token')
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'dob',
            'contact_no',
            'password',
            'message',
            'email',
            'token'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'first_name': {
                'allow_blank': True,
                'required': False
            }
        }

    def validate(self, data):
        email = data.get('email', None)
        if email is None:
            raise exceptions.ParseError(detail='Email Field is required.')
        user = User.objects.filter(email=email).count()
        if user != 1:
            raise exceptions.ParseError(detail='Email is not registered')
        return data

    def generate_token(self, obj):
        user = User.objects.get(**obj)
        tokenObject = Token.objects.update_or_create(user=user)
        return str(tokenObject[0])
