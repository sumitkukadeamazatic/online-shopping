"""
     Definitions of Custom Database managers for app 'User'
"""
from django.contrib.auth.base_user import BaseUserManager
from django.db import connection
from django.utils import timezone


class UserManager(BaseUserManager):
    """
        Custom Database Manager for 'user' table
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
           Custom create user Method
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
           Custom create superuser Method
        """
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM role WHERE slug = 'superuser'")
            result = cursor.fetchall()
            if not result:
                now = timezone.now()
                cursor.execute(
                    "INSERT INTO role(name, slug, created_at, updated_at) VALUES ('Super User', 'superuser','%s' ,'%s') RETURNING id" % (now, now))
                result = cursor.fetchall()
            for item in result:
                super_user_role_id = item[0]
                break
        extra_fields.setdefault('role_id', super_user_role_id)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
