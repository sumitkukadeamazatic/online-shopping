"""
   User App Serializers
"""
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError, AuthenticationFailed
from rest_framework.validators import UniqueValidator
from .models import Role, User, ResetPassword


class UserLoginSerializer(serializers.ModelSerializer):
    """
          User Authentication Serializer
    """
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = (
            'password',
            'email',
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

    def validate(self, data):  # pylint: disable=arguments-differ
        """
            User Authentication
        """
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise AuthenticationFailed(detail='Invalid Credentials')
        return user


class KnoxUserLoginSerializer(serializers.ModelSerializer):
    """
        Serializer used as default for knox login api
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'middle_name', 'dob', 'contact_no', 'gender', 'profile_pic')


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

    def create(self, valid_data):  # pylint: disable=arguments-differ
        password = valid_data.pop('password')
        customer_role = Role.objects.filter(slug='customer').distinct().first()
        if customer_role is None:
            now = timezone.now()
            customer_role = Role.objects.create(
                name='Customer', slug='customer', created_at=now, updated_at=now)
        valid_data.update({'role_id': customer_role.id})
        user = User.objects.create_user(password=password, **valid_data)
        return user

    def update(self, user, valid_data):  # pylint: disable=arguments-differ
        if 'password' in valid_data.keys():
            password = valid_data.pop('password')
            user.set_password(password)
            user.save()
        User.objects.filter(pk=user.id).update(**valid_data)
        return User.objects.get(pk=user.id)


class RequestResetPasswordSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    User reset password request serializer
    """
    email = serializers.EmailField()
    message = serializers.CharField(
        max_length=100, required=False, allow_blank=True)

    class Meta:
        model = ResetPassword

    def validate(self, data):  # pylint: disable=arguments-differ
        """
        User Reset Password validate
        """
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise ParseError(detail='Email doesn\'t exists.')
        return data


class ValidateResetPasswordSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Validate Reset password request Serializer
    """

    otp = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField(required=False)
    is_ouput = serializers.BooleanField(required=False)

    class Meta:
        model = ResetPassword
        fields = ['otp', 'email', 'message']
        extra_kwargs = {
            'message': {
                'read_only': True
            }
        }

    def validate(self, data):  # pylint: disable=arguments-differ
        """
        Validate API for reset password validate
        """
        requested_user = ResetPassword.objects.filter(
            user__email=data['email'], is_validated=False, otp=data['otp']).first()
        if not requested_user:
            raise ParseError(detail='Invalid data')
        now = timezone.now()
        time_diff = (now - requested_user.created_at).total_seconds()
        # OTP verification must be done in 5 mins
        if time_diff > 300.0:
            raise ParseError(detail='OTP verification timed out.')
        ResetPassword.objects.filter(id=requested_user.id).update(
            is_validated=True)
        return data


class ResetPasswordSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Reset Password Serializer
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    reset_password_id = serializers.IntegerField(required=False)

    def validate(self, data):  # pylint: disable=arguments-differ
        """
        Validate reset password data
        """
        user = User.objects.get(email=data['email'])
        if user is None:
            raise ParseError(detail='Invalid data.')
        now = datetime.now()
        possible_otp_time = now - timedelta(minutes=5)
        reset_pending = ResetPassword.objects.filter(
            user__email=data['email'], is_validated=True, is_reset=False, created_at__gte=possible_otp_time).first()
        if not reset_pending:
            raise ParseError(detail='Invalid data.')
        elif data['password'] != data['confirm_password']:
            raise ParseError(detail='Invalid data.')
        data['reset_password_id'] = reset_pending.id
        return data


class ResponseResetPasswordSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Response
    """
    message = serializers.CharField(required=True)
