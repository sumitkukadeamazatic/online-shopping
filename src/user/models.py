from django.db import models
from django.utils import timezone
from utils.models import TimestampsAbstract
# Create your models here.

   
class Role(TimestampsAbstract):
    name = models.CharField(max_length = 20, unique = True)
    slug = models.SlugField(unique = True)

    class Meta():
        db_table = 'role'



class User(TimestampsAbstract):
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length = 255, null = True, blank = True)
    last_name = models.CharField(max_length = 255, null = True, blank = True)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    gender = models.CharField(max_length = 1, null = True, blank=True)
    contact_no = models.CharField(max_length = 20, null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    profile_pic = models.TextField(null = True, blank = True)
    email = models.CharField(max_length = 255, unique = True)
    password = models.TextField()
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta():
        db_table = 'user'
        indexes = [
            models.Index(fields=['first_name','last_name','gender','dob','created_at','updated_at'], name='user_index'),
        ]


