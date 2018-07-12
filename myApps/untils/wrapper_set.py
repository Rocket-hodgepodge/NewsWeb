"""
装饰器类,访问页面,登录验证,接口访问登录验证
AUTH: TTC
DATE: 2018年7月5日 09:49:38
"""

from functools import wraps

from django.http.response import HttpResponseRedirect, JsonResponse

from myApps.untils.access_statistics import StatisticsThread


def is_login(fn):
    """
    访问页面时的登录的验证
    未登录会跳转到登录页面
    :param fn:  需要判断的方法
    :return: 返回具体页面
    """

    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.session['user_id']
            print(user_id)
        except KeyError as e:
            print('有用户未登录', str(e))
            return HttpResponseRedirect('/user_operation/login/')
        else:
            return fn(request, *args, **kwargs)

    return wrapper


def is_login_api(fn):
    """
    访问接口时调用的登录验证
    未登录会返回300
    :param fn: 需要判断的方法
    :return: 返回状态码为300的JSON数据
    """

    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            request.session['user_id']
        except KeyError:
            data = {'code': 300, 'msg': '未登录,无法访问'}
            return JsonResponse(data)
        else:
            return fn(request, *args, **kwargs)

    return wrapper


def access_total(fn):
    """
    访问量统计模块
    :param fn: 需要进行访问统计的方法
    :return:
    """
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        StatisticsThread().start()  # 启动子线程进行统计
        return fn(request, *args, **kwargs)

    return wrapper
