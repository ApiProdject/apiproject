from django.urls import path
from stands.views import *

urlpatterns = [
    path('stand/create/', StandCreateView.as_view()),
    path('all/', StandListView.as_view()),
    path('stand/', StandByEventView.as_view()),
    path('stand/recognition', ImageRecognizeView.as_view()),
    path('owner/all/', StandByUserView.as_view())
]