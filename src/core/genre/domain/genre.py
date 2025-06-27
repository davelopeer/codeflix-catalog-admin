from uuid import UUID, uuid4
from dataclasses import dataclass, field

from src.core._shared.entity import Entity


@dataclass
class Genre(Entity):
    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f'{self.name} - ({self.is_active})'

    def __repr__(self):
        return f"Genre {self.name} ({self.id})"
    
    def _validate(self):
        if len(self.name) > 255:
            self.notification.add_error('name cannot be longer than 255')

        if not self.name:
            self.notification.add_error('name cannot be empty')

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def change_name(self, name):
        self.name = name

        self._validate()
    
    def activate(self):
        self.is_active = True
        self._validate()
    
    def deactivate(self):
        self.is_active = False
        self._validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self._validate
        
    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self._validate

    def clean_categories(self):
        self.categories = set()
        self._validate
