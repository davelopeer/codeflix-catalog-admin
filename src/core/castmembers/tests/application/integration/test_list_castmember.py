from unittest.mock import create_autospec

from src.core.castmembers.infra.in_memory_castmember_repository import InMemoryCastMemberRepository
from src.core.castmembers.domain.castmember import CastMember, CastMemberType
from src.core.castmembers.application.use_cases.list_castmembers import CastMemberOutput, ListCastMember, ListCastMemberRequest, ListCastMemberResponse
from src.core.castmembers.domain.castmember_repository import CastMemberRepository


class TestListCastMembers:
    def test_when_no_cast_members_in_repository_then_return_empty_list(self):
        repository = InMemoryCastMemberRepository(cast_members=[])

        use_case = ListCastMember(repository)
        request = ListCastMemberRequest()

        response = use_case.execute(request)

        assert response == ListCastMemberResponse(data=[])

    def test_when_cast_member_in_repository_then_return_list(self):
        cast_member_one = CastMember(
            name="Adriana Esteves",
            type=CastMemberType.ACTOR
        )

        cast_member_two = CastMember(
            name="Marcos Pasquim",
            type=CastMemberType.ACTOR
        )

        repository = InMemoryCastMemberRepository(cast_members=[])
        repository.save(cast_member_one)
        repository.save(cast_member_two)

        use_case = ListCastMember(repository)
        request = ListCastMemberRequest()

        response = use_case.execute(request)

        assert response == ListCastMemberResponse(data=[
            CastMemberOutput(
                id=cast_member_one.id,
                name=cast_member_one.name,
                type=cast_member_one.type,
            ),
            CastMemberOutput(
                id=cast_member_two.id,
                name=cast_member_two.name,
                type=cast_member_two.type,
            ),
        ])
