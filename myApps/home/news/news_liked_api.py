"""
新闻点赞模块
AUTH:
DATE:

"""
from django.http.response import HttpResponse, JsonResponse
from myApps.models import NewsLiked


def hello_news_liked(request):
    return HttpResponse('Hello News Liked')


def get_news_liked_num(request):
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
            total = NewsLiked.objects.filter(news=news_id).count()
        except Exception as e:
            print(e)
            data['code'] = 4021
            data['msg'] = '请求的news_id不存在'
            return JsonResponse(data)
        else:
            data['code'] = 200
            data['msg'] = '请求成功'
            data['total'] = total
            return JsonResponse(data)


def news_liked(request):
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
