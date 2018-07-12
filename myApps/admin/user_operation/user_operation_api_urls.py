from django.urls import path

from myApps.admin.user_operation import user_operation_api

urlpatterns = [
    path('', user_operation_api.hello_user_operation),
    path('login/', user_operation_api.login),
    path('verify/<int:v_random>/', user_operation_api.set_verify),
    path('register/', user_operation_api.register),
    path('logout/', user_operation_api.logout),
    path('icon_modify/', user_operation_api.icon_modify),
    path('info_modify/', user_operation_api.info_modify)
]
