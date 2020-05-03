from django.urls import path

from matches.views import MatchByStandView

urlpatterns = [
    path('match/', MatchByStandView.as_view()),
]