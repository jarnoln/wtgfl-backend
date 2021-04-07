from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=250)
    description = models.TextField()
    color = models.CharField(max_length=20)

    def __str__(self):
        return '{}:{}'.format(self.poll.name, self.name)
