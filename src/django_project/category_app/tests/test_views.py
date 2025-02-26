import uuid
import pytest

from rest_framework import status
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return Category(
        name='Movie',
        description='Movie description'
    )

@pytest.fixture
def category_documentary():
    return Category(
        name='Documentary',
        description='Documentary description'
    )

@pytest.fixture
def category_repository() ->DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListCategoryAPI:
    def test_list_categories(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = '/api/categories/'
        response = APIClient().get(url)

        expected_data = {
            'data': [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active
                }
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        url = f'/api/categories/123123123/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        expected_data = {
            'data': {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


    def test_return_404_when_category_dont_exists(self):
        url = f'/api/categories/{uuid.uuid4()}/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = f'/api/categories/'
        response = APIClient().post(
            url,
            data={
                'name':'',
                'description':'Movie description',
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_category_then_return_201(
            self,
            category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = f'/api/categories/'
        response = APIClient().post(
            url,
            data={
                'name':'Movie',
                'description':'Movie description',
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = uuid.UUID(response.data['id'])  

        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name='Movie',
            description='Movie description'
        )


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = f'/api/categories/123123123/'
        response = APIClient().put(
            url,
            data={
                'name': '',
                'description': 'Movie description',
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            'name': ['This field may not be blank.'],
            'id': ['Must be a valid UUID.'],
            'is_active': ['This field is required.'],
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().put(
            url,
            data={
                'name': 'Documentary',
                'description': 'Documentary description',
                'is_active': True,
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == 'Documentary'
        assert updated_category.description == 'Documentary description'
        assert updated_category.is_active is True

    def test_when_category_does_no_exist_then_return_404(self):
        url = f'/api/categories/{uuid.uuid4()}/'

        response = APIClient().put(
            url,
            data={
                'name': 'Documentary',
                'description': 'Documentary description',
                'is_active': True,
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_then_retrun_400(self) -> None:
        url = f'/api/categories/123123123/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_does_not_exist_then_delete_and_return_404(self) -> None:
        url = f'/api/categories/{uuid.uuid4()}/'

        response = APIClient().delete(url)
    
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_when_category_does_exist_then_delete_and_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.list() == []


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_id_is_invalid_then_return_400(self) -> None:
        url = f'/api/categories/123123123/'
        response = APIClient().patch(
            url,
            data={
                'name': 'Movie',
                'description': 'Movie description',
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            'id': ['Must be a valid UUID.'],
        }

    def test_when_only_name_is_provided_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,    
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                'name': 'Series',
            }
        )

        updated_category = category_repository.get_by_id(id=category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_category.name == 'Series'
        assert updated_category.description == 'Movie description'
        assert updated_category.is_active is True


    def test_when_only_description_is_provided_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,    
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                'description': 'Series description',
            }
        )

        updated_category = category_repository.get_by_id(id=category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_category.name == 'Movie'
        assert updated_category.description == 'Series description'
        assert updated_category.is_active is True

    def test_when_only_is_active_is_provided_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,    
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(
            url,
            data={
                'is_active': False,
            }
        )

        updated_category = category_repository.get_by_id(id=category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_category.name == 'Movie'
        assert updated_category.description == 'Movie description'
        assert updated_category.is_active is False

    def test_when_category_doesnt_exist_return_404(self) -> None:
        url = f'/api/categories/{uuid.uuid4()}/'
        response = APIClient().patch(
            url,
            data={
                'name': 'Series',
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
