# Create your tests here.
import contextlib
from django.utils import timezone
from .models import Workshop, Card
from users.models import CustomUser
from django.test import TestCase
from random import randrange

class test_Workshop(TestCase):

    def setUp(self):
        user = CustomUser.objects.create_user(email="normal1@user2s.com", password="foo", avatar=None)
        Workshop.objects.create(pk=randrange(100,10000), workshop_name="Test workshop1", workshop_date="2050-01-03 18:00", workshop_owner=user)

    def test_work(self):
        workshop = Workshop.objects.get(workshop_name="Test workshop1")
        self.assertEqual(workshop.workshop_name, 'Test workshop1')
        self.assertEqual(workshop.is_active, True)
        self.assertEqual(workshop.workshop_owner.email, 'normal1@user2s.com')