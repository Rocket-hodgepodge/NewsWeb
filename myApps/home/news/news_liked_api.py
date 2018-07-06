"""
新闻点赞模块
AUTH:
DATE:

"""
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from myApps.models import NewsLiked, NewsArticle


def hello_news_liked(request):
    return HttpResponse('Hello News Liked')


def get_news_liked_num(request, news_id):
    """
    获取新闻点赞数
    :param request:
    :return:
    """
    if request.method == 'GET':
        data = {}
        try:
            # 获取新闻id
            news_id = request.GET.get('news_id')
            # 获取新闻点赞数
            total = NewsLiked.objects.filter(News=news_id).count()

            data['code'] = 200
            data['msg'] = '请求成功'
            data['total'] = int(total)
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data['code'] = 4021
            data['msg'] = '请求的news_id不存在'
            return JsonResponse(data)


def news_liked(request):
    """
    新闻点赞
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'news_index.html')
    if request.method == 'POST':
        data = {}
        try:
            pass
        except Exception as e:
            print(e)
            data['code'] = 4301
            data['msg'] = '点赞失败,已经点过赞,无法再次点赞'
            return JsonResponse(data)
