from unittest.mock import create_autospec

from src.core.castmembers.application.use_cases.update_castmembers import UpdateCastMember, UpdateCastMemberRequest
from src.core.castmembers.domain.castmember import CastMember, CastMemberType
from src.core.castmembers.domain.castmember_repository import CastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_name(self):
        cast_member = CastMember(
            name="Quen Tarantino",
            type=CastMemberType.DIRECTOR,
        )

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Quentin Tarantino",
        )

        response = use_case.execute(request)

        assert response is None
        mock_repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_type(self):
        cast_member = CastMember(
            name="Quentin Tarantino",
            type=CastMemberType.ACTOR,
        )

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            type=CastMemberType.DIRECTOR,
        )

        response = use_case.execute(request)

        assert response is None
        mock_repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            name="Quent Tarantino",
            type=CastMemberType.ACTOR,
        )

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Quentin Tarantino",
            type=CastMemberType.DIRECTOR,
        )

        response = use_case.execute(request)

        assert response is None
        mock_repository.update.assert_called_once_with(cast_member)