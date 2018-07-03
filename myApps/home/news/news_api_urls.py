from django.urls import path

from myApps.home.news import news_liked_api, news_operation_api

urlpatterns = [
    path('liked/', news_liked_api.hello_news_liked),
    path('', news_operation_api.hello_news_operation),
]
