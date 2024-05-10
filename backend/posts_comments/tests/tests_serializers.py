from django.test import TestCase
from django.urls import reverse

from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from posts_comments import models, serializers
from users.models import ConcertifyUser, Notification
from events.models import Event, Location, Role


class TestPostSerializer(TestCase):
    def setUp(self):
        self.serializer_class = serializers.PostSerializer
        self.factory = APIRequestFactory()
        self.owner = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.user = ConcertifyUser.objects.create(
            username='test12',
            email='test12@email.com',
            password='test'
        )
        location = Location.objects.create(
            name="test",
            address_line="test",
            city="test",
            postal_code="12-345",
            country="TST"
        )
        self.event = Event.objects.create(
            title="test",
            desc="test",
            location=location
        )
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.USER
        )
        self.data = {
            'title': 'test',
            'desc': 'test',
            'event': self.event.id
        }

    def test_send_notification_after_creation(self):
        """After post added to database, there should be a notification
          added"""
        url = reverse('posts_comments:post-list')
        request = self.factory.post(url)
        request.user = self.owner

        serializer = self.serializer_class(
            data=self.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        expedcted_notification = Notification(
            title='New post was added related to the event you are '
            'participating in.',
            desc=f'Post was added to "{serializer.validated_data["title"]}" '
            'event.',
            notification_type=Notification.TypeChoice.CASUAL
        )

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.title,
                         expedcted_notification.title)
        self.assertEqual(notification.desc,
                         expedcted_notification.desc)
        self.assertEqual(Notification.TypeChoice(int(
            notification.notification_type)),
                         expedcted_notification.notification_type)

    def test_send_notification_after_update(self):
        """After post updated, there should be a notification added"""
        url = reverse('posts_comments:post-detail',
                      kwargs={'pk': self.event.id})
        request = self.factory.put(url)

        post = models.Post.objects.create(
            title='test2',
            desc='test2',
            event=self.event)

        serializer = self.serializer_class(
            instance=post,
            data=self.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        expedcted_notification = Notification(
            title='Post was changed that is related to the event you '
            'are participating in.',
            desc=f'Post with tiltle "{serializer.validated_data["title"]}" '
            'was changed.',
            notification_type=Notification.TypeChoice.CASUAL
        )

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.title,
                         expedcted_notification.title)
        self.assertEqual(notification.desc,
                         expedcted_notification.desc)
        self.assertEqual(Notification.TypeChoice(int(
            notification.notification_type)),
                         expedcted_notification.notification_type)


class TestCommentSerializer(TestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.serializer_class = serializers.CommentSerializer
        self.factory = APIRequestFactory()
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.post = models.Post.objects.first()

    def test_validate(self):
        """Upon validating request user should be added to attrs"""
        url = reverse('posts_comments:comment-list')
        request = self.factory.post(url)
        request.user = self.user

        data = {
            'title': 'test',
            'desc': 'test',
            'post': self.post.id
        }

        serializer = self.serializer_class(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertEqual(self.user, serializer.validated_data['user'])


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
