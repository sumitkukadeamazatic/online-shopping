from rest_framework.test import APIRequestFactory, force_authenticate
from users.models import User

factory = APIRequestFactory()
user = User.objects.get(email='sumit@amazatic.com')
request = factory.get('/product/')
force_authenticate(request, user=user, token=user.auth_token)
response = view(request)

