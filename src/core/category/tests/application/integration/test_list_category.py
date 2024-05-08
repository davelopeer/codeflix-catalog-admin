from unittest.mock import create_autospec
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryRequest, ListCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategories:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
        category_filme = Category(
            name='Filme',
            description='Categoria para filmes',
        )
        category_series = Category(
            name='Serie',
            description='Categoria para series',
            is_active=True
        )
        repository = InMemoryCategoryRepository()
        repository.save(category_filme)
        repository.save(category_series)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[
            CategoryOutput(
                id=category_filme.id,
                name=category_filme.name,
                description=category_filme.description,
                is_active=category_filme.is_active
            ),
            CategoryOutput(
                id=category_series.id,
                name=category_series.name,
                description=category_series.description,
                is_active=category_series.is_active
            )
        ])
