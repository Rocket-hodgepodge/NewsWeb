from django.urls import path

from myApps.admin.admin_page import admin_page_api

urlpatterns = [
    path('', admin_page_api.hello_admin_page),
    path('admin_count/', admin_page_api.count_types),
    path('admin_time/',admin_page_api.count_news),
]
