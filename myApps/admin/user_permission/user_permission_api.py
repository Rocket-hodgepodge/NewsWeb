"""
用户权限模块
AUTH: TTC
DATE: 2018-07-12 15:10
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def hello_user_permission(request):
    return HttpResponse('Hello User Permission')


def get_role(request):
    return
