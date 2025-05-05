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

from core.genre.application.use_cases.list_genre import ListGenre
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.serializers import ListGenreOutputSerializer



class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListGenre.Input()
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input)
        serializer = ListGenreOutputSerializer(instance=output)

        return Response(
            status=HTTP_200_OK,
            data =serializer.data
        )
    
    # def retrieve(self, request: Request, pk=None) -> Response:
    #     serializer = RetrieveCategoryRequestSerializer(data={'id':pk})
    #     serializer.is_valid(raise_exception=True)        
        
    #     input = GetCategoryRequest(**serializer.validated_data)
    #     use_case = GetCategory(repository=DjangoORMCategoryRepository())

    #     try:
    #         output = use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)
        
    #     response_serializer = RetrieveCategoryResponseSerializer(instance=output)
    #     return Response(
    #         status=HTTP_200_OK,
    #         data=response_serializer.data
    #     )
    
    # def create(self, request: Request) -> Response:
    #     serializer = CreateCategoryRequestSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     input = CreateCategoryRequest(**serializer.validated_data)
    #     use_case = CreateCategory(repository=DjangoORMCategoryRepository())
    #     output = use_case.execute(request=input)

    #     return Response(
    #         status=HTTP_201_CREATED,
    #         data=CreateCategoryResponseSerializer(output).data,
    #     )

    # def update(self, request: Request, pk=None) -> Response:
    #     serializer = UpdateCategoryRequestSerializer(
    #         data={
    #             **request.data,
    #             'id':pk,
    #         }
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input = UpdateCategoryRequest(**serializer.validated_data)
    #     use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
    #     try:
    #         output = use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)
        
    #     return Response(status=HTTP_204_NO_CONTENT)

    # def destroy(self, request: Request, pk=None) -> Response:
    #     serializer = DeleteCategoryRequestSerializer(data={'id':pk})
    #     serializer.is_valid(raise_exception=True)

    #     input = DeleteCategoryRequest(**serializer.validated_data)
    #     use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

    #     try:
    #         use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(status=HTTP_204_NO_CONTENT)

    # def partial_update(self, request:Request, pk=None) -> Response:
    #     serializer = PartialUpdateRequestSerializer(
    #         data={
    #             **request.data,
    #             'id':pk
    #         }
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input = UpdateCategoryRequest(**serializer.validated_data)
    #     use_case = UpdateCategory(DjangoORMCategoryRepository())
        
    #     try:
    #         use_case.execute(request=input)
    #     except CategoryNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)
        
    #     return Response(status=HTTP_204_NO_CONTENT)