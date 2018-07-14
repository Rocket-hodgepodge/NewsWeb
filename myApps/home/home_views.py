"""
前端视图文件
AUTH: TTC
DATE: 2018年7月6日 01:47:14
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from myApps.models import NewsArticle, User, NewsType
from myApps.untils.wrapper_set import access_total


def hello_world(request):
    return HttpResponse('hello world!')


@access_total
def index(request):
    """
    前台首页
    :param request: 请求
    :return:
    """
    news_art = NewsArticle.objects.order_by('-publish_time')[:10]
    print(len(news_art))
    news_list = encapsulation_data(news_art)
    hot_art = NewsArticle.objects.order_by('-read_total')[:10]
    hot_list = encapsulation_data(hot_art)
    society_info = get_one_last_info('社会')
    newss_info = get_one_last_info('新闻')

    # try:
    #     user_id = request.session['user_id']
    #     user = User.objects.get(id=user_id)
    # except (KeyError, ObjectDoesNotExist) as e:
    #     print(connection.queries)
    #     print(e)
    # else:
    #     like_art = user.follow_type.all()
    #     for news_type in like_art:
    #         print(news_type.name)

    return render(request, 'home/index.html', context={'newsList': news_list,
                                                       'hotList': hot_list,
                                                       'society_info': society_info,
                                                       'newss_info': newss_info})


@access_total
def get_one_last_info(type_str):
    """
    获取相关类型最新的资讯信息
    :param type_str: '类型名称'
    :return: Query
    """
    news_type = NewsType.objects.filter(name=type_str).first()
    type_id = news_type.id
    news_art = NewsArticle.objects.filter(type_id=type_id).order_by('-publish_time').first()
    item = {'id': news_art.id, 'title': news_art.title}
    return item


@access_total
def encapsulation_data(query_set):
    """
    封装查询结果的方法

    :param query_set: 查询结果
    :return:list对象
    """
    news_list = []
    for article in query_set:
        item = {'id': article.pk,
                'title': article.title,
                'publish_time': article.publish_time.strftime('%Y-%m-%d')}
        news_list.append(item)
    return news_list


@access_total
def hot_news(request):
    """
    前台最热资讯榜
    :param request:
    :return:
    """
    return render(request, 'home/hot_news.html')


@access_total
def news(request):
    """
    前台最新资讯榜
    :param request:
    :return:
    """
    return render(request, 'home/news.html')


@access_total
def news_search(request):
    """
    前台新闻模糊查询
    :param request: 请求对象
    :return:
    """
    return render(request, 'home/news_search.html')


@access_total
def show_news(request, news_id):
    """
    前台单条新闻展示页面
    :param news_id: 新闻ID
    :param request:
    :return:
    """
    data = {}
    try:
        newsobj = NewsArticle.objects.get(pk=news_id)
    except ObjectDoesNotExist:
        data['title'] = ''
        data['content'] = ''
    else:
        data['id'] = news_id
        data['title'] = newsobj.title
        data['content'] = newsobj.content
        data['publish_time'] = newsobj.publish_time
        data['read_total'] = newsobj.read_total
        newsobj.read_total += 1
        newsobj.save()
    return render(request, 'home/show_news.html', {'data': data})


@access_total
def user_info(request):
    """
    前台用户信息页面,可修改用户信息
    :param request:
    :return:
    """
    return render(request, 'home/user_info.html')


@access_total
def news_type(request, type_id):
    """
    新闻类型分类页面
    :param request:
    :return:
    """
    return render(request, 'home/type_news.html')


@access_total
def get_type_count(request):
    """
    前台左边新闻分类
    :param request:
    :return:
    """
    data = {}
    type_list = []
    try:
        user_id = request.session['user_id']
    except KeyError:
        follow_list = []
    else:
        follow_set = User.objects.get(pk=user_id).follow_type.values_list('id').all()
        # print(follow_set)
        follow_list = [x[0] for x in follow_set]
    type_query = NewsArticle.objects.values_list('type_id').annotate(Count('type_id'))
    for x in type_query:
        type_item = NewsType.objects.values_list('id', 'name').get(pk=x[0])
        item = {
            'id': x[0],
            'total': x[1],
            'name': type_item[1],
            'isFollow': 1 if type_item[0] in follow_list else 0,
        }
        type_list.append(item)
    data['code'] = 200
    data['msg'] = '请求成功'
    data['type_list'] = type_list
    return JsonResponse(data)
