from django.utils import timezone

from rest_framework import mixins, viewsets

from events import permissions, serializers
from events.models import Event, SocialMedia


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.ReadOnlyPermission]


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.EventPermissions]

    def get_queryset(self):
        return Event.objects.filter(end__gt=timezone.now())

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.EventDetailsSerializer
        return serializers.EventFeedSerializer


class RoleViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.RoleSerializer


class EventContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventContactSerializer


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SocialMediaSerializer

    def get_queryset(self):
        return SocialMedia.objects.all()
