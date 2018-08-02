import os
## All the secret envornment settings 
## will be here like secret keys and passwords
## SECURITY WARNING: keep this file used in production secret!



SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = { 
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'), 
    }   
}


