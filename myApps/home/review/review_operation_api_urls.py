from django.urls import path

from myApps.home.review import review_operation_api

urlpatterns = [
    path(r'^addition/', review_operation_api.add_review, name='add_review'),
]
