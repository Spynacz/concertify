from django.test import TestCase

from users.models import ConcertifyUser


class TestConcertifyUser(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@email.com',
            'password': 'test',
            'first_name': 'Test',
            'last_name': 'TestTest'
        }
        self.user = ConcertifyUser.objects.create_user(**self.data)

    def test_get_name_method_not_none(self):
        """get_name method should return first_name and last_name"""
        self.assertEqual(
            self.user.get_name(),
            f"{self.data['first_name']} {self.data['last_name']}"
        )

    def test_get_name_method_is_none(self):
        """get_name method should return None,
           when there is not first_name and last_name data"""
        user = ConcertifyUser(
            username='test',
            password='test'
        )
        self.assertIsNone(user.get_name())
