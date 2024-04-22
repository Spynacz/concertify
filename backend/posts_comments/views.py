from rest_framework import exceptions, permissions
from rest_framework import mixins, viewsets

from events.permissions import IsEventModerator

from events.models import Role

from posts_comments import models, serializers
from posts_comments.permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return models.Post.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsEventModerator
            ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        event = serializer.validated_data.get('event')

        try:
            role = Role.objects.get(event=event, user=self.request.user)
        except Role.DoesNotExist:
            msg = "You do not have a role in related event."
            raise exceptions.PermissionDenied(msg)

        if int(role.name) < Role.NameChoice.MODERATOR:
            msg = "You do not have permission to perform this action."
            raise exceptions.PermissionDenied(msg)

        return super().perform_create(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class PostVoteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.PostVoteSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return models.PostVote.objects.all()


class CommentVoteViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.CommentVoteSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return models.CommentVote.objects.all()
