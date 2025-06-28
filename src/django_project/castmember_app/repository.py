from uuid import UUID

from src.core.castmembers.domain.castmember import CastMember
from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModelMapper.to_model(cast_member)
        cast_member_model.save()
    
    def list(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cast_member_model) for cast_member_model in self.cast_member_model.objects.all()
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
            cast_member_model = self.cast_member_model.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member_model)
        except self.cast_member_model.DoesNotExist:
            return None
        

class CastMemberModelMapper:

    @staticmethod
    def to_model(cast_member: CastMember) -> CastMemberModel:
        return CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    @staticmethod
    def to_entity(cast_member_model: CastMemberModel) -> CastMember:
        return CastMember(
            id=cast_member_model.id,
            name=cast_member_model.name,
            type=cast_member_model.type,
        )