from dataclasses import dataclass
from uuid import UUID

from src.core.castmembers.application.exceptions import CastMemberNotFound


@dataclass
class DeleteCastMemberRequest:
    id: UUID


class DeleteCastMember:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, request: DeleteCastMemberRequest) -> None:
        cast_member = self.repository.get_by_id(id=request.id)

        if cast_member is None:
            raise CastMemberNotFound(f"Cast Member with id {request.id} not found")
        
        self.repository.delete(cast_member.id)
