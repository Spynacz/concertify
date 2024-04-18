from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from events.models import Event, Role
from posts_comments import models, serializers
from users.models import ConcertifyUser


class TestVoteMixin(TestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.PostSerializer
        self.factory = APIRequestFactory()
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.post = models.Post.objects.first()

        self.event = Event.objects.first()
        Role.objects.create(event=self.event, user=self.user, name=2)

    def test_get_has_voted_not_authenticated(self):
        """When user is not authenticated has_voted will always be False"""
        url = reverse('posts_comments:post-detail',
                      kwargs={'pk': self.post.id})
        request = self.factory.get(url)
        request.user = AnonymousUser()

        serializer = self.serializer_class(
            instance=self.post,
            context={'request': request}
        )

        self.assertFalse(serializer.data.get('has_voted'))

    def test_get_has_voted_authenticated_not_voted(self):
        """When authenticated and vote doesn't exists method"""\
            """ will return False"""
        url = reverse('posts_comments:post-detail',
                      kwargs={'pk': self.post.id})
        request = self.factory.get(url)
        request.user = self.user

        serializer = self.serializer_class(
            instance=self.post,
            context={'request': request}
        )

        self.assertFalse(serializer.data.get('has_voted'))

    def test_get_has_voted_authenticated_voted(self):
        """When authenticated and vote exists method will return True"""
        models.PostVote.objects.create(user=self.user, post=self.post)
        url = reverse('posts_comments:post-detail',
                      kwargs={'pk': self.post.id})
        request = self.factory.get(url)
        request.user = self.user

        serializer = self.serializer_class(
            instance=self.post,
            context={'request': request}
        )

        self.assertTrue(serializer.data.get('has_voted'))

    def test_get_vote_count(self):
        """Method should return amount of votes for given posts"""
        url = reverse('posts_comments:post-detail',
                      kwargs={'pk': self.post.id})
        request = self.factory.get(url)
        request.user = self.user

        serializer = self.serializer_class(
            instance=self.post,
            context={'request': request}
        )

        self.assertEqual(
            serializer.data.get('vote_count'),
            self.post.votes.all().count()
        )
