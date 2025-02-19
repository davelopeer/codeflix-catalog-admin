import uuid
from unittest.mock import create_autospec

import pytest
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_category_repository import InMemoryGenreRepository


@pytest.fixture
def drama_genre():
    return Genre(name="Drama")

@pytest.fixture
def action_genre():
    return Genre(name="Action")

@pytest.fixture
def mock_genre_repository_with_categories(drama_genre, action_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = [drama_genre, action_genre]
    return repository

@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = []
    return repository

@pytest.fixture
def movie_category():
    return Category(name="Movie")

@pytest.fixture
def documentary_category():
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository



class TestListGenre:
    def test_list_genres_with_associated_categories(
            self,
            drama_genre,
            action_genre,
            mock_genre_repository_with_categories,
        ):
        use_case = ListGenre(repository=mock_genre_repository_with_categories)
        output = use_case.execute(input=None)

        assert len(output.data) == 2

        assert output.data[0].id == drama_genre.id
        assert output.data[0].name == drama_genre.name
        assert output.data[0].is_active == drama_genre.is_active
        assert output.data[0].categories == drama_genre.categories

        assert output.data[1].id == action_genre.id
        assert output.data[1].name == action_genre.name
        assert output.data[1].is_active == action_genre.is_active
        assert output.data[1].categories == action_genre.categories

    def test_empty_list_when_there_is_no_genre_saved(
            self,
            mock_empty_genre_repository,
        ):
        use_case = ListGenre(repository=mock_empty_genre_repository)

        output = use_case.execute(input=None)

        assert len(output.data) == 0
        