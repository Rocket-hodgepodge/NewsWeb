from django.urls import path

from myApps.home import home_views

urlpatterns = [
    path('', home_views.index),
]
