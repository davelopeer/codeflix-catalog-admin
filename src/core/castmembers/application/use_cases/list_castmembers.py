from dataclasses import dataclass
from uuid import UUID

from src.core.castmembers.domain.castmember_repository import CastMemberRepository
from src.core.castmembers.domain.castmember import CastMemberType


@dataclass
class ListCastMemberRequest:
    pass


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class ListCastMemberResponse:
    data: list[CastMemberOutput]

class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
        cast_members = self.repository.list()

        return ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                ) for cast_member in cast_members
            ]
        )
