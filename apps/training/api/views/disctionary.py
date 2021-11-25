from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.api.views import BaseViewSet
from apps.training import models

from ...models import Category
from .. import serializers


class DictionaryApiViewSet(
    BaseViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    serializer_map = {
        "list": serializers.UserWordSerializer,
        "create": serializers.UserWordCreateSerializer,
        "destroy": serializers.UserWordCreateSerializer,
        "add_category_words": serializers.CategoryIdSerializer,
    }
    filter_backends = [SearchFilter]
    search_fields = (
        "word__english",
        "word__russian",
    )

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.UserWord.objects.filter(
            user=self.request.user
        ).select_related("word")

    @action(methods=["POST"], detail=False, url_path="add-category-words")
    def add_category_words(self, request):
        """Add all words from category to user."""
        category_id_serializer = self.get_serializer(data=request.data)
        category_id_serializer.is_valid(raise_exception=True)
        category_id = category_id_serializer.data["category_id"]
        category = get_object_or_404(
            queryset=Category.objects.all(),
            id=category_id,
        )
        self.request.user.words.add(
            *category.words.exclude(
                id__in=self.request.user.words.values("id")
            )
        )
        return Response(status=status.HTTP_200_OK,)
