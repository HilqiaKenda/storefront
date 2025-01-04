from rest_framework import status
from store.models import Product
import pytest

@pytest.fixture
def create_product(api_client):
    def product_create(product):
        return api_client.post('/store/products/', product)
    return product_create

@pytest.fixture
def update_product(api_client):
    def do_update(product):
        return api_client.patch('/store/products/', product)
    return do_update

@pytest.mark.django_db
class TestCreateProducts:
    def test_if_user_is_not_authenticate_returns_401(self, api_client):
        response = api_client.post('/store/products/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, api_client, authenicate_user):
        authenicate_user(is_staff=False)
        response = api_client.post('/store/products/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestRerieveProduct:
    def test_if_user_is_get_returns_200(self, api_client):
        response = api_client.get('/store/products/')
        
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestUpdateProduct:
    def test_update_if_user_anonymous_retuens_405(self, authenicate_user, update_product):
        authenicate_user(is_staff=True)
        response = update_product({'title': 'G-beauty'})
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED