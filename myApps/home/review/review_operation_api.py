"""
评论/点赞/踩, 模块
AUTH:
DATE:
"""
from django.http.response import HttpResponse


def hello_review(request):
    return HttpResponse('Hello Review')
