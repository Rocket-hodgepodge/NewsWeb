from django.urls import path

from myApps.home.review import review_operation_api

urlpatterns = [
    path(r'addReview/', review_operation_api.add_review, name='add_review'),
    path(r'reviews/', review_operation_api.get_review, name='get_review'),
    path('addLiked/', review_operation_api.add_liked_review),
    path(r'deleteReview/<int:review_id>/', review_operation_api.delete_review, name='delete_rev')
]
