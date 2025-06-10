
from uuid import UUID

import pytest
from src.core.castmembers.application.exceptions import InvalidCastMemberData
from src.core.castmembers.application.use_cases.create_castmembers import CreateCastMember, CreateCastMemberRequest, CreateCastMemberResponse
from src.core.castmembers.domain.castmember import CastMemberType
from src.core.castmembers.infra.in_memory_castmember_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository)
        request = CreateCastMemberRequest(
            name="Adriana Esteves",
            type=CastMemberType.ACTOR
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateCastMemberResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == "Adriana Esteves"
        assert repository.categories[0].type == CastMemberType.ACTOR

    def test_create_cast_member_with_invalid_type(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMemberData):
            use_case.execute(CreateCastMemberRequest(name="Adriana Esteves", type="Musician"))

    def test_create_cast_member_with_invalid_name(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMemberData):
            use_case.execute(CreateCastMemberRequest(name="", type=CastMemberType.ACTOR))