from django.urls import path

from myApps.home.review import review_operation_api

urlpatterns = [
    path(r'addition/', review_operation_api.add_review, name='add_review'),
    path(r'reviews/', review_operation_api.get_review, name='get_review'),
    path(r'is_like/', review_operation_api.is_like, name='rev_is_like'),
    path(r'is_liked_add', review_operation_api.add_is_liked, name="add_is_like"),
    path(r'delete_rev', review_operation_api.delete_rev, name='delete_rev')
]
