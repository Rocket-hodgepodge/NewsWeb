from django.urls import path

from myApps.home.review import review_operation_api

urlpatterns = [
    path('', review_operation_api.hello_review),
]
