"""
后台首页
AUTH:
DATA:
"""

from django.shortcuts import render
from django.http.response import HttpResponse


def hello_admin_page(request):
    return HttpResponse('Hello Admin Page')
