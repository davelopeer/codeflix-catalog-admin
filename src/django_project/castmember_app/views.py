from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.core.castmembers.application.use_cases.delete_castmembers import DeleteCastMember, DeleteCastMemberRequest
from src.core.castmembers.application.exceptions import CastMemberNotFound
from src.core.castmembers.application.use_cases.update_castmembers import UpdateCastMember, UpdateCastMemberRequest
from src.core.castmembers.application.use_cases.create_castmembers import CreateCastMember, CreateCastMemberRequest
from src.core.castmembers.application.use_cases.list_castmembers import ListCastMember, ListCastMemberRequest
from src.django_project.castmember_app.repository import DjangoORMCastMemberRepository
from src.django_project.castmember_app.serializers import (
    CreateCastMemberResponseSerializer,
    CreateCastMemberRequestSerializer,
    DeleteCastMemberSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer
)

class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCastMemberRequest()
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(input)

        serializer = ListCastMemberResponseSerializer(instance=output)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data="Invalid data"
            )

        input = CreateCastMemberRequest(**serializer.validated_data)
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(output).data,
        )
    
    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCastMemberRequestSerializer(
            data={
                **request.data,
                "id":pk, 
            }
        )
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data="Invalid data"
            )
        
        input = UpdateCastMemberRequest(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(request=input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCastMemberSerializer(data={"id":pk})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(status=HTTP_400_BAD_REQUEST, data="Invalid data")
        
        input = DeleteCastMemberRequest(**serializer.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(request=input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)