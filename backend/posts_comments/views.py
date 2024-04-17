from rest_framework import permissions
from rest_framework import mixins, viewsets

from events.permissions import IsEventModerator

from posts_comments import models, serializers
from posts_comments.permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return models.Post.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [
                permissions.IsAuthenticated,
                IsEventModerator
            ]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == ['create', 'update', 'partial_update', 'destroy']:
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
