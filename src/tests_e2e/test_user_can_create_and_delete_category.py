import pytest

from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_delete_category(self) -> None:
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

        # Check if can get created category
        get_response = api_client.get(f'{url}{create_category_id}/')

        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data == {
            'data': {
                    'id': create_category_id,
                    'name': 'Movie',
                    'description': 'Movie description',
                    'is_active': True,
            }
        }

        # Check if can delete created category
        delete_response = api_client.delete(f'{url}{create_category_id}/')

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Check if deleted category doesn't exist
        get_response = api_client.get(f'{url}{create_category_id}/')

        assert get_response.status_code == status.HTTP_404_NOT_FOUND