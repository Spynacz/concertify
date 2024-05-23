from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from users.models import ConcertifyUser, Notification
from users.serializers import UserNotificationSerializer

from events.models import Event, Location


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


class TestUserNotificationView(APITestCase):

    def setUp(self):
        self.location = Location.objects.create(
            name='test',
            address_line='test',
            city='test',
            postal_code='test',
            country='TST'
        )
        self.user1 = ConcertifyUser.objects.create(
            username='test1',
            email='test1@email.com',
            password='TestTest'
        )
        self.user2 = ConcertifyUser.objects.create(
            username='test2',
            email='test2@email.com',
            password='TestTest'
        )
        self.user3 = ConcertifyUser.objects.create(
            username='test3',
            email='test3@email.com',
            password='TestTest'
        )
        self.event = Event.objects.create(
            title="test1",
            desc="test1",
            start=now() - timedelta(days=20),
            end=now() - timedelta(days=10),
            location=self.location
        )

        self.notification1 = Notification.objects.create(
            title='title',
            desc='desc',
            notification_type=Notification.TypeChoice.CASUAL,
            user=self.user2
        )
        self.notification2 = Notification.objects.create(
            title='title',
            desc='desc',
            notification_type=Notification.TypeChoice.CASUAL,
            user=self.user3
        )
        token = f"Token {AuthToken.objects.create(user=self.user2)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_get_notification(self):
        """Get should return all notification related with user"""
        url = reverse("users:notifications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0],
            UserNotificationSerializer(instance=self.notification1).data
        )

    def test_set_as_seen(self):
        """Put request should set has_been_seen flag as true"""
        url = reverse("users:notifications",
                      kwargs={'pk': self.notification1.id})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
