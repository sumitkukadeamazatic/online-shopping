from django.contrib.auth.base_user import BaseUserManager
from django.db import connection
from django.utils import timezone

class UserManager(BaseUserManager):
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
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM role WHERE slug = 'superuser'")
            result = cursor.fetchall()
            if len(result) == 0:
                now = timezone.now()
                cursor.execute("INSERT INTO role(name, slug, created_at, updated_at) VALUES ('Super User', 'superuser','%s' ,'%s') RETURNING id" % (now, now))
                result = cursor.fetchall()
            for item in result:
                superUserRoleId = item[0]
                break;
        extra_fields.setdefault('role_id', superUserRoleId)
        extra_fields.setdefault('is_superuser', True)        
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
