import pytest

from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()
        url = '/api/categories/'

        # Check if category list is empty
        list_response = api_client.get(url)
        assert list_response.data == {'data': []}

        # Create a category
        create_response = api_client.post(
            url,
            data={
                'name': 'Movie',
                'description': 'Movie description',
            }
        )

        assert create_response.status_code == status.HTTP_201_CREATED
        create_category_id = create_response.data['id']

        # Check if created category shows in list
        list_response = api_client.get(url)
        assert list_response.data == {
            'data': [
                {
                    'id': create_category_id,
                    'name': 'Movie',
                    'description': 'Movie description',
                    'is_active': True,
                }
            ]
        }

        # Edit created category

        update_request = api_client.put(
            f'{url}{create_category_id}/',
            data={
                'name': 'Documentary',
                'description': 'Documentary description',
                'is_active': False,
            }
        )

        assert update_request.status_code == status.HTTP_204_NO_CONTENT
        
        # Check if category is shown in list
        list_response = api_client.get(url)
        assert list_response.data == {
            'data': [
                {
                    'id': create_category_id,
                    'name': 'Documentary',
                    'description': 'Documentary description',
                    'is_active': False,
                }
            ]
        }