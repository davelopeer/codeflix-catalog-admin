from enum import StrEnum
from uuid import UUID, uuid4
from dataclasses import dataclass, field


class CastMemberType(StrEnum):
    ACTOR = "ATOR"
    DIRECTOR = "DIRETOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f'{self.name} - {self.type}'

    def __repr__(self):
        return f"CastMember {self.name} ({self.id})"

    def _validate(self):
        if len(self.name) > 255:
            raise ValueError('CastMember name cannot be longer than 255')

        if not self.name:
            raise ValueError('CastMember name cannot be empty')

        try:
            self.type = CastMemberType(self.type)
        except ValueError:
            raise ValueError('invalid type for CastMember')
        
    def update_cast_member(self, name: str = None, type: CastMemberType = None):
        if name:
            self.name = name
        if type:
            self.type = type

        self._validate()
