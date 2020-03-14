from django.urls import path
from events.views import *

urlpatterns = [
    path('event/create/', EventCreateView.as_view()),
    path('all/', EventListView.as_view())
]
