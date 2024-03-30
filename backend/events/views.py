from rest_framework import mixins, viewsets

from events import permissions, serializers


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.EventPermissions]


class RoleViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.RoleSerializer


class EventContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventContactSerializer


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
