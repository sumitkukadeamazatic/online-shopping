from django.db import models
from django.utils import timezone
# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length = 20)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'role'



class User(models.Model):
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length = 255, null = True)
    last_name = models.CharField(max_length = 255, null = True)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    gender = models.CharField(max_length = 1, null = True)
    contact_no = models.CharField(max_length = 20, null = True)
    dob = models.DateField(null = True)
    profile_pic = models.TextField(null = True)
    email = models.CharField(max_length = 255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta():
        db_table = 'user'
        indexes = [
            models.Index(fields=['first_name','last_name','gender','dob','created_at','updated_at'], name='user_index'),
        ]


