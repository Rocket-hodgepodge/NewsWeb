"""
后台首页
AUTH:
DATA:
"""

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.db import connection
from myApps.models import NewsArticle


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













