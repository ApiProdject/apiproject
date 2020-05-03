from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from events.views import *

urlpatterns = [
    path('event/create/', EventCreateView.as_view()),
    path('all/', EventListView.as_view()),
]
