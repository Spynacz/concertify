from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from users.models import ConcertifyUser


class TestLoginView(APITestCase):
    def setUp(self):
        self.url = reverse('users:knox-login')
        self.data = {
            'username': 'test',
            'password': 'test'
        }
        self.user = ConcertifyUser.objects.create_user(**self.data)

    def test_post_method_valid_data(self):
        """post method with valid data should return 200"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_invalid_data(self):
        """post method with invalid data should return 400"""
        response = self.client.post(
            self.url,
            data={
                'username': 'invalid',
                'password': 'invalid'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestManageUserView(APITestCase):
    def setUp(self):
        self.url = reverse('users:profile')
        self.data = {
            'username': 'test',
            'password': 'test'
        }
        user = ConcertifyUser.objects.create_user(**self.data)
        token = f"Token {AuthToken.objects.create(user=user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_get_object(self):
        """get_object method should return current user information"""
        response = self.client.get(self.url)
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPasswordChangeView(APITestCase):
    def setUp(self):
        self.old_password = "TestTest123"
        self.user = ConcertifyUser.objects.create(
            username="test",
            email="test@email.com",
            password=make_password(self.old_password)
        )
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_update(self):
        """Calling update methods should change password"""
        new_password = 'NewPass123'
        data = {
            'old_password': self.old_password,
            'password1': new_password,
            'password2': new_password
        }
        url = reverse("users:password-change")
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
