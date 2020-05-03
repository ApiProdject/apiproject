from django.urls import path

from persons.views import PeopleView

urlpatterns = [
    path('all/', PeopleView.as_view()),
]