"""
新闻操作模块
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from myApps.models import NewsArticle, NewsType


def hello_news_operation(request):
    return HttpResponse('Hello News Operation')


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
        if q_type and q_title:
            news_set = NewsArticle.objects.filter(q_title & q_type)[(rows * (page - 1)):rows * page]
        elif q_type:
            news_set = NewsArticle.objects.filter(q_type)[(rows * (page - 1)):rows * page]
        elif q_title:
            news_set = NewsArticle.objects.filter(q_title)[(rows * (page - 1)):rows * page]
        else:
            news_set = NewsArticle.objects.all()[(rows * (page - 1)):rows * page]
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
            content = news_item.content
            if content:
                content = content[:30] + '...'
            item = {
                'id': news_item.pk,
                'type': news_item.type.name,
                'content': content,
                'host': news_item.from_host,
                'publish_time': news_item.publish_time,
                'title': news_item.title,
                'read_total': news_item.read_total
            }
            news_list.append(item)
        data['code'] = 200
        data['msg'] = '请求成功'
        data['total'] = len(news_list)
        data['rows'] = news_list
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
                    contents = NewsArticle.objects.filter(Q(title__contains=news_title))\
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
                contents = NewsArticle.objects.all().values('id', 'title', 'publish_time')\
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
                contents = NewsArticle.objects.filter(type=type_id)\
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
def del_news(request):
    """
    删除新闻
    :param request:
    :return:
    """
    data = {}
    try:
        news_id = request.POST.get('')
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


def alter_news(request):
    """
    修改相关新闻
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = {}
        try:
            args = request.POST
            news_id = args.get('news_id')
            title = args.get('title')
            publish_time = args.get('publish_time')
            content = args.get('content')
            from_host = args.get('from_host')
            NewsArticle.objects.filter(id=news_id).update(title=title,
                                                          publish_time=publish_time,
                                                          content=content,
                                                          from_host=from_host)
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
