from abc import ABC


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, category: CastMember):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: CastMember) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: CastMember) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[CastMember]:
        raise NotImplementedError
