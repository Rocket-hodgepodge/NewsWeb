"""
前台首页
AUTH:
DATE:
"""
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from random import shuffle

from myApps.models import User, NewsArticle


def hello_home_page(request):
    return HttpResponse('Hello Home Page')


def get_follow_news(request):
    data = {}
    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    except (KeyError, ObjectDoesNotExist):
        data['code'] = 300
        data['msg'] = '未登录'
        return JsonResponse(data)
    else:
        like_art = user.follow_type.all()
        news_list = []
        for news_type in like_art:
            follow_news = NewsArticle.objects.filter(type_id=news_type.pk).order_by('-publish_time')[:10]
            for news in follow_news:
                item = {'id': news.pk,
                        'title': news.title,
                        'publish_time': news.publish_time.strftime('%Y-%m-%d')}
                news_list.append(item)
        shuffle(news_list)
        data['code'] = 200
        data['msg'] = '请求成功'
        data['data'] = news_list[:10]
        return JsonResponse(data)


