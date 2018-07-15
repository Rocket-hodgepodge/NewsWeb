"""
后台视图页面
该视图所有页面均需要登录才能访问,后续添加判断的装饰器即可
AUTH: TTC
DATE: 2018年7月5日 02:12:57
"""


from django.shortcuts import render

from myApps.untils.wrapper_set import is_login, is_manager


@is_manager
def index(request):
    return render(request, 'admin/index.html')


@is_manager
def news_manage(request):
    return render(request, 'admin/news_manage.html')


@is_manager
def review_manage(request):
    return render(request, 'admin/review_manage.html')


@is_manager
def role_manage(request):
    return render(request, 'admin/role_manage.html')


@is_manager
def per_manage(request):
    return render(request, 'admin/per_manage.html')
