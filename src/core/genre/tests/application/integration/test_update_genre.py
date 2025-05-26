import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.infra.in_memory_category_repository import InMemoryGenreRepository
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category


@pytest.fixture
def movie_category() -> Category:
    return Category(name='Movie')

@pytest.fixture
def documentary_category() -> Category:
    return Category(name='Documentary')

@pytest.fixture
def series_category() -> Category:
    return Category(name='Series')

@pytest.fixture
def category_repository(
        movie_category,
        documentary_category,
        series_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category, series_category]
    )

class TestUpdateGenre:
    def test_can_update_genre_name(self,
            movie_category,
            documentary_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            name='Drama',
            id=genre.id
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == 'Drama'
        assert updated_genre.categories == {movie_category.id, documentary_category.id}
        assert updated_genre.is_active is True


    def test_can_update_genre_categories(self,
            movie_category,
            documentary_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id}
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            categories={documentary_category.id}
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == 'Comedy'
        assert updated_genre.categories == {documentary_category.id}
        assert updated_genre.is_active is True

    def test_can_update_genre_is_active(self,
            movie_category,
            documentary_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id, documentary_category.id}
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            is_active=False
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == 'Comedy'
        assert updated_genre.categories == {movie_category.id, documentary_category.id}
        assert updated_genre.is_active is False

    def test_can_update_all_genre_fields(self,
            movie_category,
            documentary_category,
            series_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id, documentary_category.id},
            is_active=False
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name='Drama',
            is_active=True,
            categories={series_category.id, documentary_category.id}
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == 'Drama'
        assert updated_genre.categories == {series_category.id, documentary_category.id}
        assert updated_genre.is_active is True
    
    def test_should_raise_exception_if_category_id_does_not_exist(
            self,
            series_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name='Drama',
            is_active=True,
            categories={series_category.id}
        )

        with pytest.raises(GenreNotFound, match='Genre with id .* not found'):
            use_case.execute(input)

    def test_should_raise_exception_if_name_is_invalid(
            self,
            documentary_category,
            movie_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id, documentary_category.id},
            is_active=False
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name='1'*256,
            is_active=True,
            categories={movie_category.id}
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input) 

    def test_should_raise_exception_if_name_is_empty(
            self,
            documentary_category,
            movie_category,
            category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name='Comedy',
            categories={movie_category.id, documentary_category.id},
            is_active=False
        )
        genre_repository.save(genre)
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = UpdateGenre.Input(
            id=genre.id,
            name='',
            is_active=True,
            categories={movie_category.id}
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input) 

    def test_should_raise_exception_if_genre_has_inexistent_category_id(
            self,
            movie_category,
            category_repository
        ):
        genre = Genre(
            name='Action',
            categories={movie_category.id}
        )
        genre_repository = InMemoryGenreRepository()
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )

        invalid_genre_id = uuid.uuid4()
        input = UpdateGenre.Input(
            name='Drama',
            id=genre.id,
            categories={invalid_genre_id}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)
