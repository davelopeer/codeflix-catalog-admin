
from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:

    def __init__(self, repository: GenreRepository,
            category_repository: CategoryRepository):
        
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        categories_ids: set[UUID] | None = None
        is_active: bool | None = None


    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(f'Category with id {input.id} not found')

        current_name = genre.name

        if input.name is not None:
            current_name = input.name

        try:
            genre.change_name(current_name)

            if input.is_active == True:
                genre.activate()

            if input.is_active == False:
                genre.deactivate()

        except ValueError as err:
            raise InvalidGenre(err)
        
        # Handling categories ids
        if input.categories_ids:
            category_ids = {category.id for category in self.category_repository.list()}
            if not input.categories_ids.issubset(category_ids):
                raise RelatedCategoriesNotFound(
                    f'Categories not found: {input.categories_ids - category_ids}')

        current_categories = genre.categories
        if input.categories_ids is not None:
            current_categories = input.categories_ids

        try:
            genre.clean_categories()
            for category_id in current_categories:
                genre.add_category(category_id)
        except ValueError as err:
            raise InvalidGenre(err)

        self.repository.update(genre)
        