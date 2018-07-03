from django.urls import path

from myApps.admin.user_permission import user_permission_api

urlpatterns = [
    path('', user_permission_api.hello_user_permission),
]
