"""
     All models related to 'User' app, are defined here.
"""

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from utils.models import CustomBaseModelMixin
from .managers import UserManager
# Create your models here.


class Role(CustomBaseModelMixin):
    """
       This represents role table in database
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)


class User(CustomBaseModelMixin, AbstractBaseUser, PermissionsMixin):
    """
       This represents 'user' table in database.
    """
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'first_name',
                    'last_name',
                    'gender',
                    'dob'],
                name='user_index'),
        ]


class ResetPassword(CustomBaseModelMixin):
    """
         Reset Password Model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_validated = models.BooleanField(default=False)
    is_reset = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['otp'], name='reset_password_index')
        ]
