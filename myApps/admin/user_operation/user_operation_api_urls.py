from django.urls import path

from myApps.admin.user_operation import user_operation_api

urlpatterns = [
    path('', user_operation_api.hello_user_operation),
]
