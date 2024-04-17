from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from events.permissions import IsEventModerator

from posts_comments import models, serializers
from posts_comments.permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsEventModerator]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]


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
