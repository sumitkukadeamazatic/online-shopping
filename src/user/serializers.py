"""
   User App Serializers
"""
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from .models import Role, User
from django.utils import timezone


class UserLoginSerializer(serializers.ModelSerializer):
    """
          User Authentication Serializer
    """
    token = serializers.SerializerMethodField('generate_token')
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'dob',
            'contact_no',
            'password',
            'email',
            'token'
        )
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
        """
            User Authentication
        """
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise exceptions.AuthenticationFailed(detail='Invalid Credentials')
        return user

    def generate_token(self, user):
        """
           Generating Token
        """
        token_object = Token.objects.update_or_create(user=user)
        return str(token_object[0])


class UserSerializer(serializers.ModelSerializer):
    """
        User Model Serializer
    """
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())
    ])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email',
                  'dob', 'contact_no', 'password', 'profile_pic', 'gender')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, valid_data):
        password = valid_data.pop('password')
        customer_role = Role.objects.filter(slug='customer').distinct().first()
        if customer_role is None:
            now = timezone.now()
            customer_role = Role.objects.create(
                name='Customer', slug='customer', created_at=now, updated_at=now)
        valid_data.update({'role_id': customer_role.id})
        user = User.objects.create_user(password=password, **valid_data)
        return user

    def update(self, user, valid_data):
        if 'password' in valid_data.keys():
            password = valid_data.pop('password')
            user.set_password(password)
            user.save()
        User.objects.filter(pk=user.id).update(**valid_data)
        return User.objects.get(pk=user.id)


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    message = serializers.CharField(
        max_length=100, required=False, allow_blank=True)

    class Meta:
        model = User

    def validate(self, data):
        """
            User Reset Password validate
        """
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise exceptions.ParseError(detail='Email doesn\'t exists.')
        return data
