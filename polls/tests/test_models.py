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
