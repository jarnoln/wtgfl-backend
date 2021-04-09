import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from . import models


# Create your views here.
def index(request):
    return JsonResponse({})


def polls(request):
    poll_objects = models.Poll.objects.all()
    polls_json = serializers.serialize('json', poll_objects)
    return HttpResponse(polls_json, content_type='application/json')


def choices(request, poll_name):
    poll_object = get_object_or_404(models.Poll, name=poll_name)
    choice_objects = models.Choice.objects.filter(poll=poll_object)
    choices_json = serializers.serialize('json', choice_objects)
    return HttpResponse(choices_json, content_type='application/json')


def ballots(request, poll_name):
    poll_object = get_object_or_404(models.Poll, name=poll_name)
    choice_objects = models.Ballot.objects.filter(poll=poll_object)
    choices_json = serializers.serialize('json', choice_objects)
    return HttpResponse(choices_json, content_type='application/json')


@csrf_exempt
def poll(request, poll_name):
    if request.method == 'GET':
        poll_objects = models.Poll.objects.filter(name=poll_name)
        poll_json = serializers.serialize('json', poll_objects)
        return HttpResponse(poll_json, content_type='application/json')
    if request.method == 'PUT':
        poll_details = json.loads(request.body)
        # print(poll_details)
        poll_object, created = models.Poll.objects.get_or_create(name=poll_name)
        poll_object.title = poll_details['title']
        poll_object.description = poll_details['description']
        poll_object.save()
        return HttpResponse(request.body, content_type='application/json')
    return HttpResponse('Unsupported method: {}'.format(request.method))
