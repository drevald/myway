import unittest
import base64
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_trips(self):
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, 200)
        # print(response.context['trips_list'][0].glucose_level)
        # print(len(response.context['trips_list']))