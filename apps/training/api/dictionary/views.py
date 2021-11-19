from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.core.views import BaseViewMixin
from apps.training import models

from . import serializers


class DictionaryApiViewSet(
    BaseViewMixin,
    GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    serializer_map = {
        'list': serializers.UserWordSerializer,
        'create': serializers.UserWordCreateSerializer,
        'destroy': serializers.UserWordCreateSerializer,
    }
    filter_backends = [SearchFilter]
    search_fields = (
        "word__english",
        "word__russian",
    )

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action)
        if not serializer:
            return serializers.UserWordSerializer
        return serializer

    def get_queryset(self):
        return models.UserWord.objects.filter(
            user=self.request.user
        ).select_related("word")
