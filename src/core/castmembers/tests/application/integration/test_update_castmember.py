from src.core.castmembers.application.use_cases.update_castmembers import UpdateCastMember, UpdateCastMemberRequest
from src.core.castmembers.domain.castmember import CastMember, CastMemberType
from src.core.castmembers.infra.in_memory_castmember_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_name(self):
        cast_member = CastMember(
            name="Quen Tarantino",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Quentin Tarantino",
        )

        response = use_case.execute(request)

        assert response is None

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Quentin Tarantino"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_type(self):
        cast_member = CastMember(
            name="Quentin Tarantino",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            type=CastMemberType.DIRECTOR,
        )

        response = use_case.execute(request)

        assert response is None

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Quentin Tarantino"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            name="Quent Tarantino",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository)
        request = UpdateCastMemberRequest(
            id=cast_member.id,
            name="Quentin Tarantino",
            type=CastMemberType.DIRECTOR,
        )

        response = use_case.execute(request)

        assert response is None

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Quentin Tarantino"
        assert updated_cast_member.type == CastMemberType.DIRECTOR
