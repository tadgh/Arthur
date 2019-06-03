"""Arthur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from events.views import Events, Teams, HotWords, Utterances, Leaderboard

router = DefaultRouter()

router.register(r'leaderboard', Leaderboard)
router.register(r'hotwords', HotWords)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', Events.as_view()),
    path('teams/', Teams.as_view()),
    path('utterances/', Utterances.as_view()),
    path('', include(router.urls))

]
