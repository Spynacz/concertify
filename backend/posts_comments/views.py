from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from posts_comments import serializers


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer


class PostVoteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.PostVoteSerializer
    authentication_classes = [IsAuthenticated]


class CommentVoteViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.CommentVoteSerializer
    authentication_classes = [IsAuthenticated]
