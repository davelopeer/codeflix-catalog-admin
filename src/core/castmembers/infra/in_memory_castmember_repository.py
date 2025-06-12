from uuid import UUID
from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.core.castmembers.domain.castmember import CastMember


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members: list[CastMember] = None) -> None:
        self.cast_members: list[CastMember] = cast_members or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def delete(self, id: UUID) -> None:
        cast_member = self.get_by_id(id)
        if cast_member:
            self.cast_members.remove(cast_member)

    def update(self, cast_member: CastMember) -> None:
        old_cast_member = self.get_by_id(cast_member.id)
        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)

    def list(self) -> list[CastMember]:
        return [cast_member for cast_member in self.cast_members]
