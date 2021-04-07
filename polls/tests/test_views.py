import json
from django.test import TestCase
from django.urls import reverse
from polls import models


class IndexViewTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('index'), '/')

    def test_default_content(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')


class PollsViewTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('polls'), '/polls')

    def test_empty_list(self):
        response = self.client.get(reverse('polls'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_default_content(self):
        poll_1 = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        poll_2 = models.Poll.objects.create(name='wtgfd', title='Where To Go For Dinner?',
                                            description='Another example')
        response = self.client.get(reverse('polls'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['fields']['name'], poll_1.name)
        self.assertEqual(data[0]['fields']['title'], poll_1.title)
        self.assertEqual(data[0]['fields']['description'], poll_1.description)
        self.assertEqual(data[1]['fields']['name'], poll_2.name)
        self.assertEqual(data[1]['fields']['title'], poll_2.title)
        self.assertEqual(data[1]['fields']['description'], poll_2.description)
