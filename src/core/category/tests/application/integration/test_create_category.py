from uuid import UUID

import pytest
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name='Filme',
            description='Categoria para Filmes',
            is_active=True # default
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == 'Filme'
        assert repository.categories[0].description == 'Categoria para Filmes'
        assert repository.categories[0].is_active == True

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)

        with pytest.raises(InvalidCategoryData, match='Invalid data: name cannot be empty'):
            use_case.execute(CreateCategoryRequest(name=''))
        
        assert len(repository.categories) == 0