"""
新闻操作模块
"""
from datetime import datetime

from django import db
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from myApps.models import NewsArticle, NewsType, UserFollowRel
from myApps.untils.wrapper_set import is_login_api


def hello_news_operation(request):
    return HttpResponse('Hello News Operation')


def news_search(request):
    if request.method == 'GET':
        return render(request, 'home/news_search.html')


@require_GET
def integrated_query(request):
    data = {}
    q_type = None
    q_title = None
    try:
        title = request.GET.get('title')
        type_id = request.GET.get('type')
        page = request.GET.get('page')
        rows = request.GET.get('rows')
        order = request.GET.get('order')
        sort = request.GET.get('sort')
        if title:
            q_title = Q(title__contains=title)
        if type_id:
            q_type = Q(type_id=type_id)
        if not page:
            page = 1
        else:
            page = int(page)
        if not rows:
            rows = 10
        else:
            rows = int(rows)
        if order == 'desc':
            sort = '-' + sort
        if q_type and q_title:
            news_set = NewsArticle.objects.filter(q_title & q_type)
        elif q_type:
            news_set = NewsArticle.objects.filter(q_type)
        elif q_title:
            news_set = NewsArticle.objects.filter(q_title)
        else:
            news_set = NewsArticle.objects.all()
        total = news_set.count()
        if not sort == '':
            news_set = news_set.order_by(sort)
        news_set = news_set[(rows * (page - 1)):rows * page]
    except (KeyError, TypeError):
        data['code'] = 505
        data['msg'] = '参数错误'
        return JsonResponse(data)
    except Exception as e:
        data['code'] = 400
        data['msg'] = '服务器忙,请稍后再试!' + str(e)
        return JsonResponse(data)
    else:
        news_list = []
        for news_item in news_set:
            # content = news_item.content
            # if content:
            #     content = content[:30] + '...'
            item = {
                'id': news_item.pk,
                'type': news_item.type.name,
                # 'content': content,
                'host': news_item.from_host,
                'publish_time': news_item.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': news_item.title,
                'read_total': news_item.read_total
            }
            news_list.append(item)
        data['code'] = 200
        data['msg'] = '请求成功'
        data['total'] = total
        data['rows'] = news_list
        return JsonResponse(data)


@require_GET
def news_all_type(request):
    all_type = NewsType.objects.all()
    type_list = []
    for n_type in all_type:
        item = {
            'id': n_type.id,
            'name': n_type.name,
        }
        type_list.append(item)
    data = {
        'code': 200,
        'msg': '请求成功',
        'data': type_list
    }
    return JsonResponse(data)


@require_GET
def get_one_news(request, news_id):
    data = {}
    try:
        # 通过pk主键获取新闻文章
        news_obj = NewsArticle.objects.get(pk=news_id)
        news_dict = {  # 封装数据
            'id': news_obj.pk,
            'title': news_obj.title,
            'type': news_obj.type.name,
            'content': news_obj.content,
            'host': news_obj.from_host,
            'publish_time': news_obj.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'read_total': news_obj.read_total
        }
    except NewsArticle.DoesNotExist:
        data['code'] = 4401
        data['msg'] = '查询的值不存在!'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        data['data'] = news_dict
        return JsonResponse(data)


def news_title_search(request):
    """
    新闻标题搜索
    :param request:
    :return:
    """
    # if request.method == 'GET':
    #     return render(request, 'news_index.html')  # 测试用

    if request.method == 'GET':
        data = {}
        try:
            # 获取新闻标题关键词
            news_title = request.GET.get('title')
            if news_title:
                # 如果有关键词,从数据库标题双向模糊查询,获取所有相关标题及id和publish_time
                # Q(title__contains='abc')模糊查询带有abc的标题   Q(title__startwith='abc')以abc开头
                news_titles = NewsArticle.objects.filter(Q(title__contains=news_title)).values('title')
                if news_titles:
                    contents = NewsArticle.objects.filter(Q(title__contains=news_title)) \
                        .values('id', 'title', 'publish_time').order_by('-publish_time')
                    data['code'] = 200
                    data['msg'] = '请求成功'
                else:
                    # 如果查询不到关键词相关标题,返回一个空的列表
                    data['code'] = 4301
                    data['msg'] = '没有相关新闻'
                    data['title'] = []
                    return JsonResponse(data)
            else:
                # 如果关键词为空,返回所有标题
                contents = NewsArticle.objects.all().values('id', 'title', 'publish_time') \
                    .order_by('-publish_time')
                data['code'] = 200
                data['msg'] = '请求成功'
        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,请稍后再试'
            return JsonResponse(data)
        else:
            data['content'] = list(contents)
            return JsonResponse(data)
            # return render(request, 'news_show.html', {'data': data})  # 测试用


def news_type_search(request):
    """
    新闻类型搜索
    :param request:
    :return:
    """
    if request.method == 'GET':
        data = {}
        try:
            # 获取新闻类型id
            type_id = request.GET.get('id')
            news_type = NewsType.objects.filter(id=type_id)
            if news_type:
                # 获取所有相关类型新闻的id title 和 publish_time
                contents = NewsArticle.objects.filter(type=type_id) \
                    .values('id', 'title', 'publish_time').order_by('-publish_time')
                data['code'] = 200
                data['msg'] = '请求成功'
            else:
                # 如果没有相关新闻类型,返回一个空列表
                data['code'] = 4301
                data['msg'] = '没有相关新闻类型'
                data['type'] = []
                return JsonResponse(data)
        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,请稍后再试'
            return JsonResponse(data)
        else:
            data['content'] = list(contents)
            return JsonResponse(data)


@require_http_methods(['DELETE'])
def del_news(request, news_id):
    """
    删除新闻
    :param news_id:
    :param request:
    :return:
    """
    data = {}
    try:
        NewsArticle.objects.get(pk=news_id).delete()
    except KeyError:
        data['code'] = 505
        data['msg'] = '请求参数错误!'
        return JsonResponse(data)
    except ObjectDoesNotExist:
        data['code'] = 4001
        data['msg'] = '请求失败,删除的news_id不存在'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)


@require_POST
def alter_news(request):
    """
    修改相关新闻
    :param request:
    :return:
    """
    data = {}
    try:
        args = request.POST
        news_id = args.get('news_id')
        title = args.get('title')
        type_id = args.get('type_id')
        publish_time = args.get('publish_time')
        content = args.get('content')
        from_host = args.get('from_host')
        read_total = args.get('read_total')
        news_obj = NewsArticle.objects.get(pk=news_id)
        news_obj.title = title
        news_obj.type_id = type_id
        news_obj.publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        news_obj.content = content
        news_obj.from_host = from_host
        news_obj.read_total = read_total
        news_obj.save()
    except KeyError:
        data['code'] = 505
        data['msg'] = '请求参数错误!'
    except ObjectDoesNotExist:
        data['code'] = 4101
        data['msg'] = '修改失败,主键不存在!'
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
    return JsonResponse(data)


@is_login_api
def get_news_with_follow(request):
    """
    获取用户关注类型的前30条，未登录300未登录

    :param request: 请求对象
    :return: Json数据
    """
    data = {}
    user = request.session.get('user_id', None)
    try:
        follow_set = user.follow_type.value_list('id').all()
        follow_list = [x[0] for x in follow_set]
        news_set = NewsArticle.objects.filter(type_id__in=follow_list).order_by('-publish_time')[:30]
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙,请稍后再试'
        return JsonResponse(data)
    news_list = []
    for news in news_set:
        item = {
            'id': news.id,
            'title': news.title,
            'type': news.type.name,
            'publish_time': news.publish_time
        }
        news_list.append(item)
    data['code'] = 200
    data['msg'] = '请求成功'
    data['news_list'] = news_list
    return JsonResponse(data)


@require_GET
def get_news_order(request):
    """
    获取根据时间排序的新闻文章
    ：:param request: 请求对象
    :return: Json数据
    """
    data = {}
    page = request.GET.get('page', 1)
    order = request.GET.get('order', '-publish_time')
    try:
        page = int(page)
        news_set = NewsArticle.objects.all().order_by(order)[(page - 1) * 20: page * 20]
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后再试'
        return JsonResponse(data)
    news_list = []
    for news_obj in news_set:
        item = {
            'id': news_obj.id,
            'title': news_obj.title,
            'publish_time': news_obj.publish_time.strftime('%Y-%m-%d')
        }
        news_list.append(item)
    data['code'] = 200
    data['msg'] = '请求成功'
    data['news_list'] = news_list
    return JsonResponse(data)
