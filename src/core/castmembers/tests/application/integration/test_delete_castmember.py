import uuid
import pytest

from src.core.castmembers.infra.in_memory_castmember_repository import InMemoryCastMemberRepository
from src.core.castmembers.application.exceptions import CastMemberNotFound
from src.core.castmembers.application.use_cases.delete_castmembers import DeleteCastMember, DeleteCastMemberRequest
from src.core.castmembers.domain.castmember import CastMember, CastMemberType


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            name="Adirana Esteves",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=cast_member)

        use_case = DeleteCastMember(repository)
        request = DeleteCastMemberRequest(id=cast_member.id)

        assert repository.get_by_id(cast_member.id) is not None

        response = use_case.execute(request)

        assert response is None
        assert repository.get_by_id(cast_member.id) is None


    def test_when_cast_member_not_found_then_raise_exception(self):
        repository = InMemoryCastMemberRepository()


        use_case = DeleteCastMember(repository)
        request = DeleteCastMemberRequest(id=uuid.uuid4)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)
