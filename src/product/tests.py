from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.post('/product/review/product/', {'title': 'new idea'}, format='json')
