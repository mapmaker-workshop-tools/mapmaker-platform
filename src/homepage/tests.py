from django.urls import reverse
from django.test import TestCase
from django.test import Client
from .views import *
client = Client()

user_agent = {'User-agent': 'Mozilla/5.0'}

class test_public_site(TestCase):

    def test_homepage(self):
            url = reverse(index)
            resp = self.client.get(url, headers=user_agent)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('big picture', str(resp.content))
            
    def test_termsconditions(self):
            url = reverse(legal_terms)
            resp = self.client.get(url, headers=user_agent)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mapmaker.nl Terms and Conditions', str(resp.content))

    def test_privacy(self):
            url = reverse(legal_privacy)
            resp = self.client.get(url, headers=user_agent)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mapmaker.nl Privacy statement', str(resp.content)) 
            
    def test_blog(self):
            url = reverse(blog)
            resp = self.client.get(url, headers=user_agent)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Articles', str(resp.content)) 