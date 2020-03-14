from django.urls import path
from stands.views import *

urlpatterns = [
    path('stand/create/', StandCreateView.as_view()),
    path('all/', StandListView.as_view())
]