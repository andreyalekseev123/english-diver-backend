from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class BaseViewSet(GenericViewSet):
    """Base viewset for all views."""
    permission_classes = [IsAuthenticated]
    serializer_map = None

    def get_serializer_class(self):
        if not self.serializer_map:
            return self.serializer_class
        
        serializer = self.serializer_map.get(self.action, None)
        if not serializer:
            return self.serializer_class
        return serializer
