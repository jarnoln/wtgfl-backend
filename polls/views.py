from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from . import models


# Create your views here.
def index(request):
    return JsonResponse({})


def polls(request):
    poll_objects = models.Poll.objects.all()
    polls_json = serializers.serialize('json', poll_objects)
    return HttpResponse(polls_json, content_type='application/json')


def choices(request, poll_name):
    poll = get_object_or_404(models.Poll, name=poll_name)
    choice_objects = models.Choice.objects.filter(poll=poll)
    choices_json = serializers.serialize('json', choice_objects)
    return HttpResponse(choices_json, content_type='application/json')
