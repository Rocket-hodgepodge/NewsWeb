"""
用户的登录注册接口
AUTH:
DATA:
"""

from django.shortcuts import render
from django.http.response import HttpResponse


def hello_user_operation(request):
    return HttpResponse('Hello User Operation')
