from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from posts_comments.models import Post, PostVote
from users.models import ConcertifyUser


class TestIsOwner(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.user1 = ConcertifyUser.objects.create(
            username='testtest1',
            email='testtest1@email.com',
            password='testtest1'
        )
        post = Post.objects.first()
        post_vote = PostVote.objects.create(user=self.user1, post=post)
        self.url = reverse('posts_comments:post-vote-detail',
                           kwargs={'pk': post_vote.id})

    def test_not_authenticated(self):
        """Unauthenticated user shouldn't be able to acces the view"""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_is_owner(self):
        """User that is bound to the object can edit it"""
        token = f"Token {AuthToken.objects.create(user=self.user1)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_is_not_owner(self):
        """User that is not bound to the object cannot edit it"""
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
