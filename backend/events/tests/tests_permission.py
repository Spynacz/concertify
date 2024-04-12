from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from knox.models import AuthToken

from events.models import Event, Location, Role
from users.models import ConcertifyUser


class TestIsEventModerator(APITestCase):
    # TODO Missing test from related object to event
    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username="test",
            email="test@email.com",
            password="test"
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
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.url = reverse('events:event-detail',
                           kwargs={'pk': self.event.id})

    def test_permission_invalid(self):
        """Users with permission lower that moderator should be blocked"""
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        role = Role.objects.create(user=self.user, event=self.event,
                                   name=Role.NameChoice.USER)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        role.name = Role.NameChoice.STAFF
        role.save()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_valid(self):
        """Users with permission of moderator or higher should be allowed"""
        role = Role.objects.create(user=self.user, event=self.event,
                                   name=Role.NameChoice.MODERATOR)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        role.name = Role.NameChoice.OWNER
        role.save()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestIsEventOwner(APITestCase):
    def setUp(self):
        self.user = ConcertifyUser.objects.create(
            username="test",
            email="test@email.com",
            password="test"
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
        token = f"Token {AuthToken.objects.create(user=self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=token)
        self.url = reverse('events:event-detail',
                           kwargs={'pk': self.event.id})

    def test_permission_invalid(self):
        """Users with permission lower that owner should be blocked"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        role = Role.objects.create(user=self.user, event=self.event,
                                   name=Role.NameChoice.USER)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        role.name = Role.NameChoice.STAFF
        role.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        role.name = Role.NameChoice.MODERATOR
        role.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_valid(self):
        """Users with permission of owner or higher should be allowed"""
        Role.objects.create(user=self.user, event=self.event,
                            name=Role.NameChoice.OWNER)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_from_event_related_object(self):
        """Permission should work with event related object on the many side"""
        role = Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.OWNER
        )
        data = {
            'event': self.event.id,
            'user': self.user.id,
            'name': Role.NameChoice.STAFF
        }
        response = self.client.put(
            reverse("events:role-detail", kwargs={'pk': role.id}),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDestroyRolePermission(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.role = Role.objects.first()
        self.url = reverse("events:role-detail", kwargs={'pk': self.role.id})

        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )
        self.token = f"Token {AuthToken.objects.create(self.user)[-1]}"
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_delete_users_role(self):
        """User can delete his role"""
        token_value = AuthToken.objects.create(user=self.role.user)[-1]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_value}")
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_user_role_missing(self):
        """User without a role cannot try to delete other users role"""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_is_event_owner(self):
        """User with owner role can delete other users role"""
        Role.objects.create(
            user=self.user,
            event=self.role.event,
            name=Role.NameChoice.OWNER
        )
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_is_not_event_owner(self):
        """User without owner role cannot delete other users role"""
        Role.objects.create(
            user=self.user,
            event=self.role.event,
            name=Role.NameChoice.MODERATOR
        )
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
