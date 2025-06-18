from uuid import UUID

from src.core.castmembers.domain.castmember import CastMember
from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
    
    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            ) for cast_member in self.cast_member_model.objects.all()
        ]
    
    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(id=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )

    def get_by_id(self, id: UUID) -> CastMember:
        try:
            cast_member = self.cast_member_model.objects.get(id=id)
            return CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
        except self.cast_member_model.DoesNotExist:
            return None