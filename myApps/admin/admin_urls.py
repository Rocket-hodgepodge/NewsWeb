"""
后台页面路由文件
AUTH: TTC
DATE: 2018年7月5日 02:14:31
"""
from django.urls import path

from myApps.admin import admin_views

urlpatterns = [
    path('', admin_views.index),
    path('newsManage/', admin_views.news_manage),
    path('reviewManage/', admin_views.review_manage),
    path('roleManage/', admin_views.role_manage),
    path('perManage/', admin_views.per_manage),
]