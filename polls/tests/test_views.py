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


class PollViewTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('poll', args=['wtgfl']), '/poll/wtgfl/')

    def test_default_content(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?')
        response = self.client.get(reverse('poll', args=[poll.name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['name'], poll.name)
        self.assertEqual(data[0]['fields']['title'], poll.title)
        self.assertEqual(data[0]['fields']['description'], poll.description)

    def test_post_new_poll(self):
        self.assertEqual(models.Poll.objects.count(), 0)
        data = {
            'title': 'New poll',
            'description': 'This will be awesome'
        }
        response = self.client.put(reverse('poll', args=['new_poll']), data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertEqual(models.Poll.objects.count(), 1)
        poll = models.Poll.objects.first()
        self.assertEqual(poll.name, 'new_poll')
        self.assertEqual(poll.title, 'New poll')
        self.assertEqual(poll.description, 'This will be awesome')


class ChoicesViewTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('choices', args=['wtgfl']), '/poll/wtgfl/choices')

    def test_empty_list(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?')
        response = self.client.get(reverse('choices', args=[poll.name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_default_content(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?')
        choice_1 = models.Choice.objects.create(poll=poll, name='hamburger_hut', title='Hamburger Hut',
                                                description='Fancy burgers', color='#fff')
        choice_2 = models.Choice.objects.create(poll=poll, name='pizza_palace', title='Pizza Palace',
                                                description='Basic pizza', color='#aaa')
        response = self.client.get(reverse('choices', args=[poll.name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['fields']['name'], choice_1.name)
        self.assertEqual(data[0]['fields']['title'], choice_1.title)
        self.assertEqual(data[0]['fields']['description'], choice_1.description)
        self.assertEqual(data[0]['fields']['color'], choice_1.color)
        self.assertEqual(data[1]['fields']['name'], choice_2.name)
        self.assertEqual(data[1]['fields']['title'], choice_2.title)
        self.assertEqual(data[1]['fields']['description'], choice_2.description)
        self.assertEqual(data[1]['fields']['color'], choice_2.color)


class BallotsViewTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('ballots', args=['wtgfl']), '/poll/wtgfl/ballots')

    def test_empty_list(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?')
        response = self.client.get(reverse('ballots', args=[poll.name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_default_content(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?')
        choice_1 = models.Choice.objects.create(poll=poll, name='hamburger_hut', title='Hamburger Hut',
                                                description='Fancy burgers', color='#fff')
        choice_2 = models.Choice.objects.create(poll=poll, name='pizza_palace', title='Pizza Palace',
                                                description='Basic pizza', color='#aaa')
        ballot_1_choices = [choice_1.name, choice_2.name]
        ballot_2_choices = [choice_2.name, choice_1.name]
        ballot_1 = models.Ballot.objects.create(poll=poll, voter_name='voter_1', choices=json.dumps(ballot_1_choices))
        ballot_2 = models.Ballot.objects.create(poll=poll, voter_name='voter_2', choices=json.dumps(ballot_2_choices))

        response = self.client.get(reverse('ballots', args=[poll.name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['fields']['voter_name'], ballot_1.voter_name)
        self.assertEqual(data[0]['fields']['choices'], '["hamburger_hut", "pizza_palace"]')
        self.assertEqual(data[1]['fields']['voter_name'], ballot_2.voter_name)
        self.assertEqual(data[1]['fields']['choices'], '["pizza_palace", "hamburger_hut"]')
