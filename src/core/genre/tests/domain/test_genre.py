import pytest

from uuid import UUID, uuid4
from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            Genre(name='a'*256)

    def teste_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            Genre(name='')

    def test_create_genre_with_default_values(self):
        genre = Genre(name='Romance')
        assert genre.name == 'Romance'
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_created_genre_with_provided_values(self):
        genre_id = uuid4()
        categories = {uuid4(), uuid4()}
        genre = Genre(
            id=genre_id,
            name='Romance',
            is_active=False,
            categories=categories
        )
        assert genre.id == genre_id
        assert genre.name == 'Romance'
        assert genre.is_active is False
        assert genre.categories == categories

    def test_method_str(self):
        genre_id = uuid4()
        genre = Genre(
            id=genre_id,
            name='Romance',
        )
        assert str(genre) == 'Romance - (True)'

    def test_method_repr(self):
        genre_id = uuid4()
        genre = Genre(
            id=genre_id,
            name='Romance',
        )
        assert repr(genre) == f'Genre Romance ({genre_id})'

class TestChangeName:
    def test_change_name(self):
        genre = Genre(name='Romance')

        genre.change_name(name='Terror')
        
        assert genre.name == 'Terror'

    def test_when_name_is_empty(self):
        genre = Genre(name='Romance')

        with pytest.raises(ValueError, match='name cannot be empty'):
            genre.change_name(name='')


class TestActivate:

    def test_activate_genre(self):
        genre = Genre(
            name='Romance',
            is_active=False
        )

        genre.activate()

        assert genre.is_active == True

    def test_activate_active_genre(self):
        genre = Genre(
            name='Romance',
            is_active=False
        )

        genre.activate()

        assert genre.is_active == True

    def test_deactivate_genre(self):
        genre = Genre(
            name='Filme',
        )

        genre.deactivate()

        assert genre.is_active == False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        commom_id = uuid4()
        genre_1 = Genre(name='Filme', id=commom_id)
        genre_2 = Genre(name='Filme', id=commom_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        commom_id = uuid4()
        genre_1 = Genre(name='Filme', id=commom_id)
        dummy = Dummy()
        dummy.id = commom_id

        assert genre_1 != dummy


class TestAddCategory:
    def test_add_category_to_genre(self):
        category_id = uuid4()
        genre = Genre(name='Romance')

        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories

    def test_add_multiple_category_to_genre(self):
        category_id_1 = uuid4()
        category_id_2 = uuid4()
        genre = Genre(name='Romance')

        assert category_id_1 not in genre.categories
        assert category_id_2 not in genre.categories
        genre.add_category(category_id_1)
        genre.add_category(category_id_2)
        assert category_id_1 in genre.categories
        assert category_id_2 in genre.categories


class TestRemoveCategory:
    def test_remove_category_to_genre(self):
        category_id = uuid4()
        genre = Genre(name='Romance', categories={category_id})

        genre.remove_category(category_id)
        assert category_id not in genre.categories

class TestCleanCategories:
    def test_clean_all_categories(self):
        category_id = uuid4()
        genre = Genre(name='Romance', categories={category_id})

        genre.clean_categories()
        assert genre.categories == set()