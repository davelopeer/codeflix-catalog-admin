from enum import StrEnum
from uuid import UUID, uuid4
from dataclasses import dataclass, field

from src.core._shared.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ATOR"
    DIRECTOR = "DIRETOR"


@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f'{self.name} - {self.type}'

    def __repr__(self):
        return f"CastMember {self.name} ({self.id})"

    def _validate(self):
        if len(self.name) > 255:
            self.notification.add_error('CastMember name cannot be longer than 255')

        if not self.name:
            self.notification.add_error('CastMember name cannot be empty')

        try:
            CastMemberType(self.type)
        except ValueError:
            self.notification.add_error('invalid type for CastMember')
        
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
    def update_cast_member(self, name: str = None, type: CastMemberType = None):
        if name:
            self.name = name
        if type:
            self.type = type

        self._validate()
