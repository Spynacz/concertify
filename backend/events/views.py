from rest_framework import mixins, viewsets

from events import serializers


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer


class RoleViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.RoleSerializer


class EventContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventContactSerializer


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer
