"""
新闻点赞模块
AUTH:
DATE:

"""
from django.http.response import HttpResponse


def hello_news_liked(request):
    return HttpResponse('Hello News Liked')
