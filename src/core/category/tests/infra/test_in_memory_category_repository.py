import uuid

import pytest
from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name='Filme',
            description='Categoria para filmes'
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetById:
    def test_can_get_category(self):
        category_filme = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True
        )
        category_series = Category(
            name='Serie',
            description='Categoria para series',
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )
        

        response = repository.get_by_id(category_filme.id)

        assert response == category_filme

    def test_cannot_found_category_with_invalid_id(self):
        category_filme = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme]
        )
        

        response = repository.get_by_id(uuid.uuid4())

        assert response == None


class TestGetById:
    def test_delete_category(self):
        category_filme = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True
        )
        category_series = Category(
            name='Serie',
            description='Categoria para series',
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )
        
        assert len(repository.categories) == 2
        assert repository.categories[0].id == category_filme.id
        response = repository.delete(category_filme.id)

        assert len(repository.categories) == 1
        assert repository.categories[0].id == category_series.id
        assert response is None

    def test_cannot_delete_category_with_invalid_id(self):
        category_filme = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme]
        )
        
        assert len(repository.categories) == 1
        assert repository.categories[0].id == category_filme.id
        response = repository.delete(uuid.uuid4())

        assert len(repository.categories) == 1
        assert repository.categories[0].id == category_filme.id
        assert response == None