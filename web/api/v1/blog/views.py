from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.models import Article
from . import serializers


# @swagger_auto_schema(operation_summary="Returns all the model's objects with pagination.")

class ArticleListView(GenericAPIView, SwaggerAutoSchema):
    serializer_class = serializers.ArticleListSerializer

    def get_queryset(self):
        return Article.objects.all()

    @swagger_auto_schema(operation_summary="Show all records.")
    def get(self, request):
        """Returns all the model's objects with pagination."""
        queryset = self.get_queryset()
        serializer_instance = self.get_serializer(instance=queryset, many=True)
        paginated_data = self.paginate_queryset(serializer_instance.data)

        return self.get_paginated_response(paginated_data)


# class ArticleListViewSet(ModelViewSet):  # Использовалось для изучения работы с ModelViewSet и ViewSet в целом.
#     queryset = Article.objects.all()
#     serializer_class = serializers.ArticleListSerializer
#

