from dataclasses import dataclass
from uuid import UUID

from src.core.castmembers.application.exceptions import InvalidCastMemberData
from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.core.castmembers.domain.castmember import CastMember, CastMemberType


@dataclass
class CreateCastMemberRequest:
    name: str
    type: CastMemberType

@dataclass
class CreateCastMemberResponse:
    id: UUID


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: CreateCastMemberRequest) -> CreateCastMemberResponse:
        try:
            cast_member = CastMember(
                name=request.name,
                type=request.type,
            )
        except ValueError as err:
            raise InvalidCastMemberData("Invalid data: " + str(err))
        
        self.repository.save(cast_member)

        return CreateCastMemberResponse(id=cast_member.id)