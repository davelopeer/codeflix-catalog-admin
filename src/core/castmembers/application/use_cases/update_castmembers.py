from dataclasses import dataclass
from uuid import UUID

from src.core.castmembers.application.exceptions import CastMemberNotFound, InvalidCastMemberData
from src.core.castmembers.domain.castmember_repository import CastMemberRepository


@dataclass
class UpdateCastMemberRequest:
    id: UUID
    name: str | None = None
    type: str | None = None


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: UpdateCastMemberRequest) -> None:
        cast_member = self.repository.get_by_id(id=request.id)

        if cast_member is None:
            raise CastMemberNotFound(f"Cast Member with id {request.id} not found")
        
        current_name = cast_member.name
        current_type = cast_member.type

        if request.name is not None:
            current_name = request.name
        
        if request.type is not None:
            current_type = request.type

        try:
            cast_member.update_cast_member(
                name=current_name,
                type=current_type,
            )
        except ValueError as err:
            raise InvalidCastMemberData(err)
        
        self.repository.update(cast_member)