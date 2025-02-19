import uuid

import pytest

from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_category_repository import InMemoryGenreRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
            self,
            movie_category,
            documentary_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        new_category = Category(name="Series")
        input = use_case.Input(
            name="Romance",
            category_ids={new_category.id}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)
        

    def test_create_genre_without_categories(
        self,
        category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        input = use_case.Input(
            name="Romance",
            category_ids=set(),
        )

        output = use_case.execute(input)

        assert isinstance(output.id, uuid.UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Romance"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True

