from django.urls import path

from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('polls', views.polls, name='polls'),
   path('poll/<slug:poll_name>/', views.poll, name='poll'),
   path('poll/<slug:poll_name>/choices', views.choices, name='choices'),
]