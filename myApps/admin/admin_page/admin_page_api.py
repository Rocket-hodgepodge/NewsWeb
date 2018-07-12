"""
后台首页
AUTH:
DATA:
"""
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.db import connection
from myApps.models import NewsArticle,User
from myApps.untils.access_statistics import RedisControl






def hello_admin_page(request):
    return HttpResponse('Hello Admin Page')


def count_types(request):
    # request.session
    cursor = connection.cursor()
    cursor.execute('Select count(a.id) total, b.name from News_article a right join News_type b on b.id=a.type_id group by type_id;')
    a = cursor.fetchall()
    news_list = []
    for i in range(len(a)):
        news_dict = {'value': a[i][0], 'name': a[i][1]}
        news_list.append(news_dict)
    data = {'code': 200, 'count_types': news_list}
    return JsonResponse(data)


def count_news(request):
    data = {}
    date_list = []

    my_date = datetime.today()
    a = NewsArticle.objects.filter(publish_time__gt=my_date).count()
    date_str = my_date.strftime('%Y-%m-%d')
    item = {'value': a, 'name': date_str}
    date_list.append(item)
    for i in range(4):
        temp = my_date
        my_date -= timedelta(days=1)
        a = NewsArticle.objects.filter(publish_time__gte=my_date, publish_time__lte=temp).count()
        date_str = my_date.strftime('%Y-%m-%d')
        item = {'value': a, 'name': date_str}
        date_list.append(item)

    data['code'] = 200
    data['msg'] = '请求成功'
    data['datas'] = date_list

    return JsonResponse(data)


def active_user(request):
    data = {}
    date_list = []

    my_date = datetime.today()
    b = User.objects.filter(last_login_time=my_date).count()

    date_str = my_date.strftime('%Y-%m-%d')
    item = {'value': b, 'name': date_str}
    date_list.append(item)
    for i in range(4):
        temp = my_date
        my_date -= timedelta(days=1)
        b = User.objects.filter(last_login_time__gte=my_date, last_login_time__lte=temp).count()
        date_str = my_date.strftime('%Y-%m-%d')
        item = {'value': b, 'name': date_str}
        date_list.append(item)

    data['code'] = 200
    data['msg'] = 'ok'
    data['datas'] = date_list

    return JsonResponse(data)


def web_user(request):
    control = RedisControl()
    my_date = datetime.today()
    value_list = []
    name_list = []
    for i in range(5):
        date_str = my_date.strftime('%Y-%m-%d')
        name_list.append(date_str)
        value = control.get_access_total(date_str)
        value_list.append(value)
        my_date -= timedelta(days=1)
    data = {
        'code': 200,
        'msg': 'ok',
        'name': name_list[::-1],
        'value': value_list[::-1],
    }
    return JsonResponse(data)








