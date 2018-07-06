"""
前端视图文件
AUTH: TTC
DATE: 2018年7月6日 01:47:14
"""

from django.shortcuts import render
from django.http.response import HttpResponse


def hello_world(request):
    return HttpResponse('hello world!')


def index(request):
    """
    前台首页
    :param request:
    :return:
    """
    return render(request, 'home/index.html')


def hot_news(request):
    """
    前台最热资讯榜
    :param request:
    :return:
    """
    return render(request, 'home/hot_news.html')


def news(request):
    """
    前台最新资讯榜
    :param request:
    :return:
    """
    return render(request, 'home/news.html')


def news_search(request):
    """
    前台新闻模糊查询
    :param request:
    :return:
    """
    return render(request, 'home/news_search.html')


def show_news(request):
    """
    前台单条新闻展示页面
    :param request:
    :return:
    """
    return render(request, 'home/show_news.html')


def user_info(request):
    """
    前台用户信息页面,可修改用户信息
    :param request:
    :return:
    """
    return render(request, 'home/user_info.html')
