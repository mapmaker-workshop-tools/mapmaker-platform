# Create your tests here.
import contextlib

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo", avatar=None)
        assert user.email == "normal@user.com"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        with contextlib.suppress(AttributeError):
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert user.username is None
        #log in the user
        c = Client()
        logged_in = c.login(username="normal@user.com", password='foo')
        self.assertTrue(logged_in) 

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo", avatar=None)
        assert admin_user.email == "super@user.com"
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser
        with contextlib.suppress(AttributeError):
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert admin_user.username is None

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)

    def test_login(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo", avatar=None)
        c = Client()
        logged_in = c.login(username="normal@user.com", password='foo')
        self.assertTrue(logged_in) 