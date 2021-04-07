from django.http import HttpResponse, JsonResponse
from django.core import serializers
from . import models


# Create your views here.
def index(request):
    return JsonResponse({})


def polls(request):
    poll_objects = models.Poll.objects.all()
    polls_json = serializers.serialize('json', poll_objects)
    return HttpResponse(polls_json, content_type='application/json')
