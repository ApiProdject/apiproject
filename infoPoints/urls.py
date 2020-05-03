from django.urls import path
from infoPoints.views import InfoPointListView


urlpatterns = [
    path('all/', InfoPointListView.as_view()),
]