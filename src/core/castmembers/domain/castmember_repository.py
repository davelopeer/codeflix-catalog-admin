from abc import ABC, abstractmethod
from uuid import UUID

from src.core.castmembers.domain.castmember import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, castmember: CastMember):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: CastMember) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[CastMember]:
        raise NotImplementedError
