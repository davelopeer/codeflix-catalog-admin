import pytest

from src.core.castmembers.domain.castmember import CastMember, CastMemberType
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.django_project.castmember_app.models import CastMember as CastMemberModel


@pytest.fixture
def cast_member_actor():
    return CastMember(
        name="Adriana Esteves",
        type=CastMemberType.ACTOR,
    )

@pytest.fixture
def cast_member_director():
    return CastMember(
        name="Walter Salles",
        type=CastMemberType.DIRECTOR,
    )


@pytest.mark.django_db
class TestSaveCastMemberRepository:
    def test_save_cast_member_in_database(self, cast_member_actor):
        repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        repository.save(cast_member_actor)
        assert CastMemberModel.objects.count() == 1

        cast_member_db = CastMemberModel.objects.first()

        assert cast_member_db.id == cast_member_actor.id
        assert cast_member_db.name == cast_member_actor.name
        assert cast_member_db.type == cast_member_actor.type


@pytest.mark.django_db
class TestListCastMemberRepository:
    def test_list_cast_members_from_database(
            self,
            cast_member_actor,
            cast_member_director
        ):

        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member_actor)
        repository.save(cast_member_director)

        cast_members_db = repository.list()

        assert len(cast_members_db) == 2
        assert cast_members_db[0].id == cast_member_actor.id
        assert cast_members_db[0].name == cast_member_actor.name
        assert cast_members_db[0].type == cast_member_actor.type
        assert cast_members_db[1].id == cast_member_director.id
        assert cast_members_db[1].name == cast_member_director.name
        assert cast_members_db[1].type == cast_member_director.type


@pytest.mark.django_db
class TestDeleteCastMemberRepository:
    def test_delete_cast_member_in_database(self, cast_member_actor):
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member_actor)

        assert CastMemberModel.objects.count() == 1

        repository.delete(id=cast_member_actor.id)

        assert CastMemberModel.objects.count() == 0


@pytest.mark.django_db
class TestUpdateCastMemberRepository:
    def test_update_cast_member_name_in_database(self, cast_member_actor):
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member_actor)

        assert CastMemberModel.objects.count() == 1

        cast_member_actor.name = "Marcos Pasquim"
        repository.update(cast_member_actor)

        assert CastMemberModel.objects.first().name == "Marcos Pasquim"
        assert CastMemberModel.objects.first().type == CastMemberType.ACTOR

    def test_update_cast_member_type_in_database(self, cast_member_director):
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member_director)

        assert CastMemberModel.objects.count() == 1

        cast_member_director.type = CastMemberType.ACTOR
        repository.update(cast_member_director)

        assert CastMemberModel.objects.first().name == "Walter Salles"
        assert CastMemberModel.objects.first().type == CastMemberType.ACTOR
