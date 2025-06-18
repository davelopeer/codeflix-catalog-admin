from rest_framework import serializers

from src.core.castmembers.domain.castmember import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return CastMemberType(data)

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))


class CastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class ListCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(many=True)


class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()


class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=False)
    type = CastMemberTypeField(required=False)


class DeleteCastMemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()