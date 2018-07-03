from django.urls import path

from myApps.home.home_page import home_page_api

urlpatterns = [
    path('', home_page_api.hello_home_page),
]
