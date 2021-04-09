import json

from django.test import TestCase
from polls import models


class PollModelTest(TestCase):
    def test_can_save_and_load(self):
        poll = models.Poll(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        poll.save()
        self.assertEqual(models.Poll.objects.all().count(), 1)
        self.assertEqual(models.Poll.objects.all()[0], poll)

    def test_string(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        self.assertEqual(str(poll), poll.name)


class ChoiceModelTest(TestCase):
    def test_can_save_and_load(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        choice = models.Choice(poll=poll, name='hamburger_hut', title='Hamburger Hut', description='Fancy burgers')
        choice.save()
        self.assertEqual(models.Choice.objects.all().count(), 1)
        self.assertEqual(models.Choice.objects.all()[0], choice)

    def test_string(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        choice = models.Choice.objects.create(poll=poll, name='hamburger_hut', title='Hamburger Hut',
                                              description='Fancy burgers')
        self.assertEqual(str(choice), 'wtgfl:hamburger_hut')


class BallotModelTest(TestCase):
    def test_can_save_and_load(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        ballot = models.Ballot(poll=poll, voter_name='voter_1', choices=json.dumps([]))
        ballot.save()
        self.assertEqual(models.Ballot.objects.all().count(), 1)
        self.assertEqual(models.Ballot.objects.all()[0], ballot)

    def test_string(self):
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        ballot = models.Ballot.objects.create(poll=poll, voter_name='voter_1', choices=json.dumps({}))
        self.assertEqual(str(ballot), 'wtgfl:voter_1')

    def test_encoding(self):
        ballot_choices = [
            'pizza_palace',
            'hamburger_hut'
        ]
        poll = models.Poll.objects.create(name='wtgfl', title='Where To Go For Lunch?', description='Example poll')
        ballot = models.Ballot.objects.create(poll=poll, voter_name='voter_1', choices=json.dumps(ballot_choices))
        self.assertEqual(str(ballot), 'wtgfl:voter_1')
        choices_out = json.loads(ballot.choices)
        self.assertEqual(len(choices_out), 2)
        self.assertEqual(choices_out[0], 'pizza_palace')
        self.assertEqual(choices_out[1], 'hamburger_hut')
