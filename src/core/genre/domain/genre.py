from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: UUID = field(default_factory=uuid4) # call uuid4() everytime a new instance is created
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f'{self.name} - ({self.is_active})'

    def __repr__(self):
        return f"Genre {self.name} ({self.id})"
    
    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id
    
    def _validate(self):
        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255')

        if not self.name:
            raise ValueError('name cannot be empty')

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
