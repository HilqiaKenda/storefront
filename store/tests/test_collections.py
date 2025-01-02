from rest_framework import status
from rest_framework.test import APIClient

class TestCreateCollections:
    def test_if_user_is_anonymous(self):
        # AAA (Arrange, Act, Assert)
        # Arrange: where we preare our system under test "create object, put database, iniatial state etc.."
        
        
        # Act: this where we pput the behavior we want to test
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})
        
        # Assert: this is we see the behavior we epect 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        