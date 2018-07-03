"""
用户权限模块
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def hello_user_permission(request):
    return HttpResponse('Hello User Permission')
