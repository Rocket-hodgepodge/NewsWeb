"""
新闻操作模块
"""
from django.contrib.sites import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

from myApps.models import NewsArticle, NewsType


def hello_news_operation(request):
    return HttpResponse('Hello News Operation')


def news_search(request):
    if request.method == 'GET':
        return render(request, 'home/news_search.html')


def news_title_search(request):
    """
    新闻标题搜索
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'news_index.html')

    if request.method == 'POST':
        data = {}
        try:
            # 获取新闻标题关键词
            news_title = request.POST.get('title')
            if news_title:
                # 如果有关键词,从数据库标题双向模糊查询,获取所有相关标题及id和publish_time
                # Q(title__contains='abc')模糊查询带有abc的标题   Q(title__startwith='abc')以abc开头
                news_titles = NewsArticle.objects.filter(Q(title__contains=news_title)).values('title')
                if news_titles:
                    contents = NewsArticle.objects.filter(Q(title__contains=news_title)).values('id', 'title', 'publish_time')
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
                contents = NewsArticle.objects.all().values('id', 'title', 'publish_time')
                data['code'] = 200
                data['msg'] = '请求成功'

            data['content'] = list(contents)
            return render(request, 'news_show.html', {'data': data})

            # p = Paginator(titles_list_all, 10)  # titles_list分页,每页10行
            # p.count  # 数据总数
            # p.num_pages  # 总页数
            # p.page_range  # 得到页码,动态生成
            # page_num = requests.GET.get("page")  # 以get的方法从url地址中获取
            # try:
            #     titles_list = p.page(page_num)  # 显示指定页码的数据
            # except PageNotAnInteger:  # 如果输入页码错误，就显示第一页
            #     titles_list = p.page(1)
            # except EmptyPage:  # 如果超过了页码范围，就把最后的页码显示出来，
            #     titles_list = p.page(p.num_pages)
            # return render(requests, "news_show.html", locals())

        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,请稍后再试'
            return JsonResponse(data)


def news_type_search(request):
    """
    新闻类型搜索
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'news_type.html')

    if request.method == 'POST':
        data = {}
        try:
            # 获取新闻类型id
            type_id = request.POST.get('id')
            if type_id:
                # 获取所有相关类型新闻的id title 和 publish_time
                contents = NewsArticle.objects.filter(type=type_id).values('id', 'title', 'publish_time')
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

        data['content'] = list(contents)
        return render(request, 'news_show.html', {'data': data})


def del_news(request):
    """
    删除新闻
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = {}
        try:
            pass
        except Exception as e:
            print(e)
            data['code'] = 4001
            data['msg'] = '请求失败,删除的news_id不存在'
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
            pass
        except Exception as e:
            print(e)
            data['code'] = 4101
            data['msg'] = '修改失败,主键不存在'
            return JsonResponse(data)
