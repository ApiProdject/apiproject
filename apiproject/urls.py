"""apiproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth', include('rest_framework.urls')),
    path('api/v1/users', include('users.urls')),
    path('api/v1/persons', include('persons.urls')),
    path('api/v1/photos', include('photos.urls')),
    path('api/v1/events', include('events.urls')),
    path('api/v1/stands', include('stands.urls')),
    path('api/v1/user_stands', include('user_stands.urls')),
    path('api/v1/emotionTypes', include('emotionTypes.urls')),
    path('api/v1/infoPoints', include('infoPoints.urls')),
    path('api/v1/matches', include('matches.urls')),
]
