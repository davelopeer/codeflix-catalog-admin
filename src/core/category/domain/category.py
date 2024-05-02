from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Category:
    name: str
    description: str = ''
    is_active: bool = True
    id: UUID = field(default_factory=uuid4) # call uuid4() everytime a new instance is created

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f'{self.name} - {self.description} ({self.is_active})'

    def __repr__(self):
        return f"Category {self.name} ({self.id})"
    
    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id
    
    def _validate(self):
        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255')

        if not self.name:
            raise ValueError('name cannot be empty')

    def update_category(self, name, description):
        self.name = name
        self.description = description

        self._validate()
    
    def activate(self):
        self.is_active = True
        self._validate()
    
    def deactivate(self):
        self.is_active = False
        self._validate()
