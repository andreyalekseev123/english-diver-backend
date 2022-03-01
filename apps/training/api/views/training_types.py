from django.http import Http404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from apps.core.api.views import BaseViewSet
from apps.training import models
from apps.training.api import serializers
from apps.training.constants import TRAINING_TYPES_PROCESSORS_MAPPING


class TrainingTypeViewSet(BaseViewSet, ListModelMixin):
    """ViewSet for training type."""
    queryset = models.TrainingType.objects.all()
    serializer_class = serializers.TrainingTypeSerializer

    serializer_map = dict(
        default=serializers.TrainingTypeSerializer,
        start=serializers.TrainingItemSerializer,
        finish=serializers.FinishTrainingSerializer,
    )

    @action(
        detail=True,
        methods=["POST"],
    )
    def start(self, request, pk=None):
        """Start training."""
        training_type: models.TrainingType = self.get_object()
        processor = TRAINING_TYPES_PROCESSORS_MAPPING[training_type.id](
            training_type=training_type,
            user=request.user,
        )
        is_enough_words = processor.check_enough_words()
        if not is_enough_words:
            error_message = processor.get_not_enough_words_error_message()
            raise ValidationError(error_message)

        serializer = self.get_serializer(
            processor.generate_data_for_training(),
            many=True,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["POST"],
    )
    def finish(self, request, pk=None):
        """Finish training."""
        training_type: models.TrainingType = self.get_object()
        training = models.Training.objects.filter(
            type=training_type,
            user=request.user,
        ).select_related("type").prefetch_related(
            "questions",
            "questions__user_word",
            "questions__user_word__word",
        ).first()
        if not training:
            raise Http404
        serializer = self.get_serializer(
            training=training,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
