from django.urls import path
from users.views import *

urlpatterns = [
    path('user/create/', UserCreationView.as_view()),
]