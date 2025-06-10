

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.castmembers.application.exceptions import InvalidCastMemberData
from src.core.castmembers.application.use_cases.create_castmembers import CreateCastMember, CreateCastMemberRequest, CreateCastMemberResponse
from src.core.castmembers.domain.castmember import CastMemberType
from src.core.castmembers.domain.castmember_repository import CastMemberRepository


class TestCreateCastMembers:
    def test_create_cast_members_with_valid_data(self):
        mock_repository = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=mock_repository)
        request = CreateCastMemberRequest(
            name="Adriana Esteves",
            type=CastMemberType.ACTOR
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCastMemberResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_cast_member_with_invalid_type(self):
        use_case = CreateCastMember(repository=MagicMock(CastMemberRepository))

        with pytest.raises(InvalidCastMemberData):
            use_case.execute(CreateCastMemberRequest(name="Adriana Esteves", type="Musician"))

    def test_create_cast_member_with_invalid_name(self):
        use_case = CreateCastMember(repository=MagicMock(CastMemberRepository))

        with pytest.raises(InvalidCastMemberData):
            use_case.execute(CreateCastMemberRequest(name="", type=CastMemberType.ACTOR))