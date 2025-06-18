import pytest

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestE2ECastMember:
    def test_user_can_create_and_edit_and_delete_category(self) -> None:
        api_client = APIClient()
        url = "/api/castmembers/"

        # Check if cast member list is empty
        list_response = api_client.get(url)
        assert list_response.data == {"data": []}

        # Create a cast member
        create_response = api_client.post(
            url,
            data={
                "name": "Adriana Esteves",
                "type": "ATOR",
            }
        )

        assert create_response.status_code == status.HTTP_201_CREATED
        create_cast_member_id = create_response.data['id']

        # Check if created cast member shows in list
        list_response = api_client.get(url)
        assert list_response.data == {
            'data': [
                {
                    'id': create_cast_member_id,
                    'name': "Adriana Esteves",
                    'type': 'ATOR',
                }
            ]
        }

        # Edit created cast member

        update_request = api_client.put(
            f'{url}{create_cast_member_id}/',
            data={
                'name': 'Quentin Tarantino',
                "type": "DIRETOR"
            }
        )

        assert update_request.status_code == status.HTTP_204_NO_CONTENT
        
        # Check if cast member is shown in list
        list_response = api_client.get(url)
        assert list_response.data == {
            'data': [
                {
                    'id': create_cast_member_id,
                    'name': 'Quentin Tarantino',
                    "type": "DIRETOR"
                }
            ]
        }

        # Check if can delete created cast member
        delete_response = api_client.delete(f'{url}{create_cast_member_id}/')

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Check if deleted cast member doesn't exist
        get_response = api_client.get(f'{url}')
        assert get_response.data == {"data": []}