import pytest
from src.core.castmembers.domain.castmember import CastMember, CastMemberType


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            CastMember(type=CastMemberType.ACTOR)

    def test_type_is_required(self):
        with pytest.raises(TypeError):
            CastMember(name="John Travolta")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember(name="a"*256, type=CastMemberType.ACTOR)

    def test_name_should_not_be_empty(self):
        with pytest.raises(ValueError, match="CastMember name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_type_should_be_valid(self):
        with pytest.raises(ValueError, match="invalid type for CastMember"):
            CastMember(name="Jack Johnson", type="MUSICO")

    def test_create_castmember_with_provided_values(self):
        cast_member = CastMember(name="Adriana Esteves", type=CastMemberType.ACTOR)

        assert cast_member.name == "Adriana Esteves"
        assert cast_member.type == CastMemberType.ACTOR

    def test_method_str(self):
        cast_member = CastMember(name="Adriana Esteves", type=CastMemberType.ACTOR)

        assert str(cast_member) == "Adriana Esteves - ATOR"

    def test_method_repr(self):
        cast_member = CastMember(name="Walter Salles", type=CastMemberType.DIRECTOR)

        assert repr(cast_member) == f"CastMember Walter Salles ({cast_member.id})"



class TestUpdateCastMember:

    def test_update_cast_member_with_invalid_name_should_throw_error(self):
        cast_member = CastMember(name="Adriana Esteves", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            cast_member.update_cast_member(name="a"*256)

    def test_update_cast_member_with_invalid_type_should_throw_error(self):
        cast_member = CastMember(name="Adriana Esteves", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="invalid type for CastMember"):
            cast_member.update_cast_member(type="FIGURANTE")