from django.http import Http404

from rest_framework import permissions
from rest_framework import mixins, viewsets

from events.permissions import IsEventModerator

from posts_comments import models, serializers
from posts_comments.mixins import IsEventModeratorPerformCreateMixin
from posts_comments.permissions import IsOwner


# TODO add test for the mixin  based on this view
class PostViewSet(IsEventModeratorPerformCreateMixin,
                  viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        event = self.request.query_params.get("event")
        if event:
            return models.Post.objects.filter(event=event)\
                .order_by("-created_at")
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post = self.request.query_params.get("post")
        if post:
            return models.Comment.objects.filter(post=post)\
                .order_by("-created_at")
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

    def get_object(self):
        post = self.request.data.get('post')
        try:
            return models.PostVote.objects.get(
                post=post,
                user=self.request.user
            )
        except models.PostVote.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return models.PostVote.objects.all()


class CommentVoteViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.CommentVoteSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        comment = self.request.data.get('comment')
        try:
            return models.CommentVote.objects.get(
                comment=comment,
                user=self.request.user
            )
        except models.CommentVote.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return models.CommentVote.objects.all()
