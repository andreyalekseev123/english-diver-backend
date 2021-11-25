from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from apps.core.api.views import BaseViewSet
from apps.training.models import Category

from .. import serializers


class CategoryViewSet(BaseViewSet, ListModelMixin, RetrieveModelMixin):
    """ViewSet for category model"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
