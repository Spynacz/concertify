from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory

from knox.models import AuthToken

from events import permissions
from events.models import Event, EventContact, Location, Role
from users.models import ConcertifyUser


class TestIsEventModerator(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission_check = permissions.IsEventModerator()
        self.user = ConcertifyUser.objects.create(username="test")
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
        self.url = reverse('events:event-detail',
                           kwargs={'pk': self.event.id})

    def test_invalid_for_user_without_a_role(self):
        """User without a related role do not have access"""
        request = self.factory.patch(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertFalse(permission)

    def test_invalid_for_user_with_too_low_permision(self):
        """User without at least moderator permission do not have access"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.STAFF
        )
        request = self.factory.patch(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertFalse(permission)

    def test_valid(self):
        """User with at least moderator permission have access"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        request = self.factory.patch(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertTrue(permission)

    def test_from_event_related_object(self):
        """Permission should work with event related object on the many side"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        event_contact = EventContact.objects.create(
            name="test",
            event=self.event
        )
        url = reverse(
            "events:event-contact-detail",
            kwargs={'pk': event_contact.id}
        )

        request = self.factory.patch(url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            event_contact
        )

        self.assertTrue(permission)


class TestIsEventOwner(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission_check = permissions.IsEventOwner()
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

    def test_invalid_for_user_without_a_role(self):
        """User without a related role do not have access"""
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertFalse(permission)

    def test_invalid_for_user_with_too_low_permision(self):
        """User without at least moderator permission do not have access"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.MODERATOR
        )
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertFalse(permission)

    def test_valid(self):
        """User with at least moderator permission have access"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.OWNER
        )
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.event
        )

        self.assertTrue(permission)

    def test_from_event_related_object(self):
        """Permission should work with event related object on the many side"""
        Role.objects.create(
            event=self.event,
            user=self.user,
            name=Role.NameChoice.OWNER
        )
        user_role = Role.objects.create(
            event=self.event,
            user=ConcertifyUser.objects.create(username="test-temp"),
            name=Role.NameChoice.USER
        )
        url = reverse(
            "events:role-detail",
            kwargs={'pk': user_role.id}
        )

        request = self.factory.patch(url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            user_role
        )

        self.assertTrue(permission)


class TestDestroyRolePermission(APITestCase):
    fixtures = ['fixtures/test_fixture.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission_check = permissions.DestroyRolePermission()
        self.role = Role.objects.first()
        self.url = reverse("events:role-detail", kwargs={'pk': self.role.id})

        self.user = ConcertifyUser.objects.create(
            username='test',
            email='test@email.com',
            password='test'
        )

    def test_delete_users_role(self):
        """User can delete his role"""
        request = self.factory.delete(self.url)
        request.user = self.role.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.role
        )

        self.assertTrue(permission)

    def test_request_user_role_missing(self):
        """User without a role cannot try to delete other users role"""
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.role
        )

        self.assertFalse(permission)

    def test_user_is_event_owner(self):
        """User with owner role can delete other users role"""
        Role.objects.create(
            user=self.user,
            event=self.role.event,
            name=Role.NameChoice.OWNER
        )
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.role
        )

        self.assertTrue(permission)

    def test_user_is_not_event_owner(self):
        """User without owner role cannot delete other users role"""
        Role.objects.create(
            user=self.user,
            event=self.role.event,
            name=Role.NameChoice.MODERATOR
        )
        request = self.factory.delete(self.url)
        request.user = self.user

        permission = self.permission_check.has_object_permission(
            request,
            None,
            self.role
        )

        self.assertFalse(permission)
