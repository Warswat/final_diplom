from django.test import TestCase
from rest_framework.test import APIRequestFactory

from backend.views import ShopView

# Create your tests here.

factory = APIRequestFactory()
class TestShopView(TestCase):
    fixtures = ['user.json', 'shop.json', 'category.json']

    def test_get(self):
        request = factory.get('/api/v1/shops/')
        view = ShopView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            'name': 'test',
            'state': True,
        }
        request = factory.post('/api/v1/shops/', data)
        view = ShopView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

