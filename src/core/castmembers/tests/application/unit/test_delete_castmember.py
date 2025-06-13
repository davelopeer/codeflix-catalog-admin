import uuid
import pytest
from unittest.mock import create_autospec


from src.core.castmembers.application.exceptions import CastMemberNotFound
from src.core.castmembers.application.use_cases.delete_castmembers import DeleteCastMember, DeleteCastMemberRequest
from src.core.castmembers.domain.castmember import CastMember, CastMemberType
from src.core.castmembers.domain.castmember_repository import CastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            name="Adirana Esteves",
            type=CastMemberType.ACTOR,
        )

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(mock_repository)
        request = DeleteCastMemberRequest(id=cast_member.id)

        response = use_case.execute(request)

        assert response is None
        mock_repository.delete.assert_called_once_with(cast_member.id)

    def test_when_cast_member_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCastMember(mock_repository)
        request = DeleteCastMemberRequest(id=uuid.uuid4)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)
        
        mock_repository.delete.assert_not_called()
