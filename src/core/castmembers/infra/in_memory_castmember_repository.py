from uuid import UUID
from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.core.castmembers.domain.castmember import CastMember


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, categories: list[CastMember] = None) -> None:
        self.categories: list[CastMember] = categories or []

    def save(self, category: CastMember) -> None:
        self.categories.append(category)

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        if category:
            self.categories.remove(category)

    def update(self, category: CastMember) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)

    def list(self) -> list[CastMember]:
        return [category for category in self.categories]
