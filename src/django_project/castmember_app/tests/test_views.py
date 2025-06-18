import uuid
import pytest

from rest_framework import status
from rest_framework.test import APIClient

from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.core.castmembers.domain.castmember import CastMember, CastMemberType


@pytest.fixture
def cast_member_actor():
    return CastMember(
        name="Adriana Esteves",
        type=CastMemberType.ACTOR,
    )

@pytest.fixture
def cast_member_director():
    return CastMember(
        name="Walter Salles",
        type=CastMemberType.DIRECTOR,
    )

@pytest.fixture
def repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()

@pytest.mark.django_db
class TestListCastMemberAPI:
    def test_list_cast_members(
        self,
        repository,
        cast_member_actor,
        cast_member_director,
    ):
        repository.save(cast_member_actor)
        repository.save(cast_member_director)

        url = "/api/castmembers/"
        response = APIClient().get(url)

        expected_data = {
            'data': [
                {
                    "id": str(cast_member_actor.id),
                    "name": cast_member_actor.name,
                    "type": cast_member_actor.type
                },
                {
                    "id": str(cast_member_director.id),
                    "name": cast_member_director.name,
                    "type": cast_member_director.type
                }
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateCastMemberAPI:
    def test_create_cast_member_success(
        self,
        cast_member_actor,
    ):
        url = "/api/castmembers/"
        response = APIClient().post(url, {
                "name":cast_member_actor.name,
                "type": "ATOR"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

    def test_create_cast_member_with_invalid_type(
        self,
        cast_member_actor,
    ):
        url = "/api/castmembers/"
        response = APIClient().post(url, {
                "name":cast_member_actor.name,
                "type": "MUSICO"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_cast_member_with_empty_type(
        self,
        cast_member_actor,
    ):
        url = "/api/castmembers/"
        response = APIClient().post(url, {
                "name":cast_member_actor.name,
                "type": ""
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = "/api/castmembers/123123123/"
        response = APIClient().put(
            url,
            data={
                "name": "",
                "type": "ATOR"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

    def test_when_payload_is_valid_then_update_and_return_204(
        self,
        repository,
        cast_member_actor,
    ):
        repository.save(cast_member_actor)

        url = f"/api/castmembers/{cast_member_actor.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Quentin Tarantino",
                "type": "DIRETOR"
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_cast_member = repository.get_by_id(cast_member_actor.id)

        assert updated_cast_member.name == "Quentin Tarantino"
        assert updated_cast_member.type == "DIRETOR"

    def test_when_update_only_name_then_return_204(
        self,
        repository,
        cast_member_actor,
    ):
        repository.save(cast_member_actor)

        url = f"/api/castmembers/{cast_member_actor.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Quentin Tarantino",
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_cast_member = repository.get_by_id(cast_member_actor.id)

        assert updated_cast_member.name == "Quentin Tarantino"
        assert updated_cast_member.type == "ATOR"

    def test_when_update_only_type_then_return_204(
        self,
        repository,
        cast_member_actor,
    ):
        repository.save(cast_member_actor)

        url = f"/api/castmembers/{cast_member_actor.id}/"
        response = APIClient().put(
            url,
            data={
                "type": "DIRETOR",
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_cast_member = repository.get_by_id(cast_member_actor.id)

        assert updated_cast_member.name == "Adriana Esteves"
        assert updated_cast_member.type == "DIRETOR"


    def test_when_category_does_no_exist_then_return_404(self):
        url = f"/api/castmembers/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Adriana",
                "type": "ATOR"
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_then_retrun_400(self):
        url = f"/api/castmembers/123123123/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_does_not_exist_then_delete_and_return_404(self):
        url = f"/api/castmembers/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_does_exist_then_delete_and_return_204(
        self,
        repository,
        cast_member_actor,
    ):
        repository.save(cast_member_actor)

        url = f"/api/castmembers/{cast_member_actor.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert repository.list() == []
