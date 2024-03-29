from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from rest_framework.serializers import ValidationError

from users.models import ConcertifyUser
from users.serializers import AuthSerializer, UserSerializer


class TestUserSerializer(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'TestTest123',
        }

    def test_create_method(self):
        """create method chould create new user."""
        serializer = UserSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertIsNotNone(ConcertifyUser.objects.get(
            username=self.data['username']
        ))

    def test_password_field_is_write_only(self):
        """Password field should be write only."""
        serializer = UserSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        with self.assertRaises(KeyError):
            serializer.data['password']


class TestAuthSerializer(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'password': 'test'
        }
        self.user = ConcertifyUser.objects.create_user(**self.data)

    def test_validate_valid_data(self):
        """Given valid data validate method should authenticate user."""
        serializer = AuthSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(self.user, serializer.validated_data['user'])

    def test_validate_invalid_data(self):
        """Given invalid data validdate method should raise ValidationError."""
        serializer = AuthSerializer(data={
            'username': 'invalid',
            'password': 'invalid'
        })
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            str(serializer.errors['non_field_errors'][0]),
            _('Unable to log in with provided credentials.')
        )
