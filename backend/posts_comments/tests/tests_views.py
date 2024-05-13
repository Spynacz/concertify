from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from events.models import Role
from posts_comments import models, serializers
from users.models import ConcertifyUser


class TestPostViewSet(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='TestTest'
        )
        self.post = models.Post.objects.first()
        self.serializer = serializers.PostSerializer(instance=self.post)
        self.token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.url_list = reverse('posts_comments:post-list')
        self.url_detail = reverse('posts_comments:post-detail',
                                  kwargs={'pk': self.post.id})
        self.data = {
            'title': 'New',
            'desc': 'test post',
            'picture': '',
            'event': self.post.event.id
        }

    def test_list(self):
        """Not authenticated user should be able to access post list"""
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_details(self):
        """Not authenticated user should be able to access post details"""
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, self.serializer.data)

    def test_create(self):
        """Only user with at least moderator permission can create posts"""
        Role.objects.create(
            event=self.post.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url_list, data=self.data)

        self.data.update({'picture': None})

        self.assertDictContainsSubset(self.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        """Only user with at least moderator permission can delete posts"""
        Role.objects.create(
            event=self.post.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        """Only user with at least moderator permission can update posts"""
        Role.objects.create(
            event=self.post.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(self.url_detail, data=self.data)

        self.data.update({'picture': None})

        self.assertDictContainsSubset(self.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """Only user with at least moderator permission can patch posts"""
        Role.objects.create(
            event=self.post.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        data = {'title': 'PATCH'}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(self.url_detail, data=data)

        self.assertDictContainsSubset(data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCommentViewSet(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='TestTest'
        )
        self.post = models.Post.objects.first()
        self.comment = models.Comment.objects.create(
            title='test',
            desc='test',
            post=self.post,
            user=self.user
        )
        self.token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.url_list = reverse('posts_comments:comment-list')
        self.url_detail = reverse('posts_comments:comment-detail',
                                  kwargs={'pk': self.comment.id})
        self.data = {
            'title': 'New',
            'desc': 'test comment',
            'post': self.comment.post.id,
        }
        self.serializer = serializers.CommentSerializer(instance=self.comment)

    def test_list(self):
        """Not authenticated user should be able to access comment list"""
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_details(self):
        """Not authenticated user should be able to access comment details"""
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, self.serializer.data)

    def test_create(self):
        """Authenticated user can create comments"""
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(self.url_list, data=self.data)

        self.assertDictContainsSubset(self.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        """User that created a comment can delete it"""
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        """User that created a comment can update it"""
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(self.url_detail, data=self.data)

        self.assertDictContainsSubset(self.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        """User that created a comment can patch it"""
        data = {'title': 'PATCH'}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(self.url_detail, data=data)

        self.assertDictContainsSubset(data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostVoteViewSet(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='TestTest'
        )
        self.post = models.Post.objects.first()
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_create(self):
        """Authenticated user can create comment vote"""
        url = reverse('posts_comments:post-vote-list')
        data = {'post': self.post.id}
        response = self.client.post(url, data=data)

        self.assertDictContainsSubset(data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        """User that created a post vote can delete it"""
        models.PostVote.objects.create(
            user=self.user,
            post=self.post
        )
        data = {'post': self.post.id}
        url = reverse('posts_comments:post-vote-list')
        response = self.client.delete(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCommentVoteViewSet(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='TestTest'
        )
        self.comment = models.Comment.objects.first()
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_create(self):
        """Authenticated user can create comment vote"""
        url = reverse('posts_comments:comment-vote-list')
        data = {'comment': self.comment.id}
        response = self.client.post(url, data=data)

        self.assertDictContainsSubset(data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        """User that created a comment vote can delete it"""
        models.CommentVote.objects.create(
            user=self.user,
            comment=self.comment
        )
        data = {'comment': self.comment.id}
        url = reverse('posts_comments:comment-vote-list')
        response = self.client.delete(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
