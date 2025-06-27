import pytest

from uuid import UUID, uuid4
from src.core.category.domain.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            Category(name='a'*256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name='Filme')
        assert isinstance((category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category(name='Filme')
        assert category.name == 'Filme'
        assert category.description == ''
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name='Filme')
        assert category.is_active is True

    def test_created_category_with_provided_values(self):
        category_id = uuid4()
        category = Category(
            id=category_id,
            name='Filme',
            description='Filmes em geral',
            is_active=False,
        )
        assert category.id == category_id
        assert category.name == 'Filme'
        assert category.description == 'Filmes em geral'
        assert category.is_active is False

    def test_method_str(self):
        category_id = uuid4()
        category = Category(
            id=category_id,
            name='Filme',
            description='Filmes em geral',
        )
        assert str(category) == 'Filme - Filmes em geral (True)'

    def test_method_repr(self):
        category_id = uuid4()
        category = Category(
            id=category_id,
            name='Filme',
        )
        assert repr(category) == f'Category Filme ({category_id})'

    def teste_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            Category(name='')

    def test_description_must_have_less_than_1024_characters(self):
        with pytest.raises(ValueError, match='description cannot be longer than 1024'):
            Category(name='Filme', description='*'*1025)

    def test_description_longer_than_1024_and_name_longer_than_255(self):
        with pytest.raises(ValueError, match='name cannot be longer than 255; description cannot be longer than 1024'):
            Category(name='*'*256, description='*'*1025)


class TestUpdateCategory:

    def test_update_category_with_name_and_description(self):
        category = Category(name='Filme', description='Filmes em geral')

        category.update_category(name='Série', description='Séries em geral')

        assert category.name == 'Série'
        assert category.description == 'Séries em geral'

    def test_update_category_with_invalid_name(self):
        category = Category(name='Filme', description='Filmes em geral')

        with pytest.raises(ValueError, match='name cannot be longer than 255'):
            category.update_category(name='a'*256, description='Séries em geral')


class TestActivate:

    def test_activate_category(self):
        category = Category(
            name='Filme',
            description='Filmes em geral',
            is_active=False
        )

        category.activate()

        assert category.is_active == True

    def test_activate_active_category(self):
        category = Category(
            name='Filme',
            description='Filmes em geral',
            is_active=False
        )

        category.activate()

        assert category.is_active == True

    def test_deactivate_category(self):
        category = Category(
            name='Filme',
            description='Filmes em geral',
        )

        category.deactivate()

        assert category.is_active == False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        commom_id = uuid4()
        category_1 = Category(name='Filme', id=commom_id)
        category_2 = Category(name='Filme', id=commom_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        commom_id = uuid4()
        category_1 = Category(name='Filme', id=commom_id)
        dummy = Dummy()
        dummy.id = commom_id

        assert category_1 != dummy
