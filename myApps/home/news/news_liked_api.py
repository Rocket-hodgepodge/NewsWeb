"""
新闻点赞模块
AUTH:
DATE:

"""
from django import db
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from myApps.models import NewsLiked
from myApps.untils.wrapper_set import is_login_api


def hello_news_liked(request):
    return HttpResponse('Hello News Liked')


@require_GET
def get_news_liked_num(request):
    """
    获取新闻的点赞数量
    :param request: 请求对象
    :return: JSON数据
    """
    data = {}
    news_id = request.GET.get('news_id', None)
    if not news_id:
        data['code'] = 504
        data['msg'] = '参数错误'
        return JsonResponse(data)
    try:
        num = NewsLiked.objects.filter(news_id=news_id).count()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后再试！'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        data['num'] = num
        return JsonResponse(data)


def news_liked1(request):
    """
    新闻点赞
    :param request:
    :return:
    """
    if request.method == 'GET':
        data = {}
        try:
            # 获取news_id 和 user_id
            news_id = request.GET.get('news_id')
            user_id = request.session.get('user_id')
            # 从NewsLiked表中查询news_id 和user_id是否同时存在于一行
            is_news_and_use = NewsLiked.objects.filter(news=news_id, use=user_id)
            if is_news_and_use:
                data['code'] = 4301
                data['msg'] = '点赞失败,已经点过赞,无法再次点赞'
            else:
                NewsLiked.objects.create(news=news_id, use=user_id)
                data['code'] = 200
                data['msg'] = '点赞成功'
        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,请稍后再试'
            return JsonResponse(data)
        else:
            return JsonResponse(data)


@require_POST
@is_login_api
def news_liked(request, user_id):
    """
    新闻点赞
    :param user_id: 用户ID
    :param request:
    :return:
    """
    data = {}
    news_id = request.POST.get('news_id', None)
    if not news_id:
        data['code'] = 504
        data['msg'] = '参数错误'
        return JsonResponse(data)
    try:
        action = NewsLiked.objects.filter(news_id=news_id, use_id=user_id).count()
        if action:
            data['code'] = 4301
            data['msg'] = '新闻点赞失败，请勿重复点击'
            return JsonResponse(data)
        NewsLiked(news_id=news_id, use_id=user_id).save()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后再试！'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)

