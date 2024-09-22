import pytest
from django.contrib.contenttypes.models import ContentType
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, force_authenticate

from backend.models import User, ConfirmEmailToken, Shop, Product, ProductInfo, Category, Contact, Order


@pytest.fixture
def client():
    client = APIClient(enforce_csrf_checks=True)
    User.objects.create_superuser(email='test@test.ru', password='test', username='test',type='shop')
    user = User.objects.get(email='test@test.ru')
    Shop.objects.create(user=user, state=True, name='test')
    client.force_authenticate(user=user)
    return client


#
# @pytest.fixture
# def token(user):
#     token = Token.objects.create(user=user)  # Create token.
#     return token


@pytest.mark.django_db
def test_partner_update(client):
    response = client.post('/api/v1/partner/update', {'url': 'https://ya.ru'}, format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_partner_state(client):
    response = client.post('/api/v1/partner/state', {'state': 'off'}, format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_partner_orders(client):
    response = client.get('/api/v1/partner/orders')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_register(client):
    response = client.post('/api/v1/user/register', {'email': 'test2@test.ru', 'password': 'test1234A', 'first_name': 'test','last_name': 'testov','company':'asdasd','position':'lead'}, format='json')
    assert response.json()['Status']

@pytest.mark.django_db
def test_user_register_confirm(client):
    client.post('/api/v1/user/register',
                {'email': 'test2@test.ru', 'password': 'test1234A', 'first_name': 'test', 'last_name': 'testov',
                 'company': 'asdasd', 'position': 'lead'}, format='json')
    token = ConfirmEmailToken.objects.get(user = User.objects.get(email='test2@test.ru'))
    response = client.post('/api/v1/user/register/confirm', {'email': 'test2@test.ru', 'token': token.key}, format='json')
    assert response.json()['Status']

@pytest.mark.django_db
def test_user_details(client):
    response = client.get('/api/v1/user/details')
    assert response.json()['email'] == 'test@test.ru'

@pytest.mark.django_db
def test_user_contact(client):
    response = client.post('/api/v1/user/contact', {'city': 'test', 'street': 'test', 'phone': 'test'}, format='multipart')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_login(client):
    response = client.post('/api/v1/user/login', {'email': 'test@test.ru', 'password': 'test'}, format='json')
    assert response.json()['Status']

@pytest.mark.django_db
def test_user_password_reset(client):
    response = client.post('/api/v1/user/password_reset', {'email': 'test@test.ru'}, format='json')
    assert response.json()['Status']

@pytest.mark.django_db
def test_user_password_reset_confirm(client):
    User.objects.create_user(email='test1@test.ru', password='qwer1234AA', username='test1',type='shop',is_active = True    , company = 'test', position = 'test')
    ResetPasswordToken(user = User.objects.get(email='test1@test.ru'),key = '123').save()
    r = client.post('/api/v1/user/password_reset/confirm', {'email': 'test1@test.ru', 'token': '123', 'password': 'qwer1234A'}, format='json')
    response = client.post('/api/v1/user/login', {'email': 'test1@test.ru', 'password': 'qwer1234A'}, format='json')
    assert r.status_code == 200 and response.json()['Status']



@pytest.mark.django_db
def test_categories(client):
    response = client.get('/api/v1/categories')
    assert response.json()['count'] == 0

@pytest.mark.django_db
def test_shops(client):
    response = client.get('/api/v1/shops')
    assert response.json()['count'] == 1

@pytest.mark.django_db
def test_products(client):
    response = client.get('/api/v1/products')
    assert response.json() == []

@pytest.mark.django_db
def test_basket(client):
    Category(name='test').save()
    Product(name='test', category=Category.objects.get(name='test')).save()
    payload = {'items': '[{"product_info": 1, "quantity": 1}]'}
    ProductInfo(model='X2',product=Product.objects.get(name='test'), external_id=1, shop=Shop.objects.get(name='test'), price=100,price_rrc=200, quantity=1).save()
    response = client.post('/api/v1/basket', payload, format='json')
    assert response.json()['Создано объектов'] == 1

@pytest.mark.django_db
def test_order():
    client = APIClient(enforce_csrf_checks=True)
    User.objects.create_superuser(email='test2@test.ru', password='test', username='test2', type='shop')
    user = User.objects.get(email='test2@test.ru')
    Shop.objects.create(user=user, state=True, name='test')
    client.force_authenticate(user=user)
    Contact(user = User.objects.get(email='test2@test.ru'),city='test', street='test', phone='+34534534523',house='test', structure='test', building='test', apartment='test').save()
    Order(contact = Contact.objects.get(city='test'),user = User.objects.get(email='test2@test.ru'), state='new').save()
    response = client.post('/api/v1/order', {'contact':Contact.objects.get(city='test').id, 'id':str(Order.objects.get(user = User.objects.get(email='test2@test.ru')).id)}, format='json')
    assert response.json()['Status'] == True


