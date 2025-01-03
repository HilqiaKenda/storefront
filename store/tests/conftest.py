from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenicate_user(api_client):
    def authentification(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return authentification