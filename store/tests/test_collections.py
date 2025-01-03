from store.models import Collection
from django.contrib.auth.models import User 
from rest_framework import status
from model_bakery import baker
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection



@pytest.mark.django_db
class TestCreateCollections:
    
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns401(self, create_collection):
        # AAA (Arrange, Act, Assert)
        # Arrange: where we preare our system under test "create object, put database, iniatial state etc.."
        
        # Act: this where we pput the behavior we want to test
        response = create_collection({'title': 'G-beauty'})
        
        # Assert: this is we see the behavior we epect 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, create_collection, authenicate_user):
        authenicate_user()
        response = create_collection({'title': 'G-beauty'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_data_is_invalid_returns_400(self, create_collection, authenicate_user):
        authenicate_user(is_staff=True)
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    @pytest.mark.skip
    def test_if_data_is_valid_returns_201(self, create_collection, authenicate_user):
        authenicate_user(is_staff=True)
        response = create_collection({'title': 'G-beauty'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data ['id'] > 0
        
        
@pytest.mark.django_db
class TestretieveCollection:
    def test_if_collection_exist_returns_200(self, api_client):
        # Arrange: where we preare our system under test "create object, put database, iniatial state etc.."
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        
        # print(collection.__dict__)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'product_count': 0
        }