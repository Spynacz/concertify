from rest_framework import mixins, viewsets

from posts_comments import serializers
from posts_comments.permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer


class PostVoteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.PostVoteSerializer
    authentication_classes = [IsOwner]


class CommentVoteViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.CommentVoteSerializer
    authentication_classes = [IsOwner]
