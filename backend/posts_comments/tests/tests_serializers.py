from django.test import TestCase
from django.urls import reverse

from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from posts_comments import models, serializers
from users.models import ConcertifyUser


class TestPostVoteSerializer(TestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.PostVoteSerializer
        self.factory = APIRequestFactory()
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.post = models.Post.objects.first()

    def test_create_unique(self):
        """User can create unique PostVote"""
        request = self.factory.post(reverse('posts_comments:post-vote-list'))
        request.user = self.user

        serializer = self.serializer_class(
            data={'post': self.post.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

    def test_create_nonunique(self):
        """User cannot create vote multiple times on one post"""
        request = self.factory.post(reverse('posts_comments:post-vote-list'))
        request.user = self.user
        models.PostVote.objects.create(post=self.post, user=self.user)

        serializer = self.serializer_class(
            data={'post': self.post.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        with self.assertRaisesMessage(ValidationError,
                                      "Object with given data already exists"):
            serializer.save()


class TestCommentVoteSerializer(TestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.CommentVoteSerializer
        self.factory = APIRequestFactory()
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.comment = models.Comment.objects.first()

    def test_create_unique(self):
        """User can create unique CommentVote"""
        request = self.factory.post(
            reverse('posts_comments:comment-vote-list'))
        request.user = self.user

        serializer = self.serializer_class(
            data={'comment': self.comment.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

    def test_create_nonunique(self):
        """User cannot create vote multiple times on one comment"""
        request = self.factory.post(
            reverse('posts_comments:comment-vote-list'))
        request.user = self.user
        models.CommentVote.objects.create(comment=self.comment, user=self.user)

        serializer = self.serializer_class(
            data={'comment': self.comment.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        with self.assertRaisesMessage(ValidationError,
                                      "Object with given data already exists"):
            serializer.save()
