"""
用户关注类型接口，获取相关关注的新闻咨询接口
AUTH: TTC
DATE: 2018.7.11 17：35

"""
from django import db
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from myApps.models import User, UserFollowRel, NewsType, NewsArticle
from myApps.untils.wrapper_set import is_login_api


@require_POST
@is_login_api
def add_follow_type(request):
    data = {}
    user_id = request.session['user_id']
    type_id = request.POST.get('type_id', None)
    if not type_id:
        data['code'] = 505
        data['msg'] = '参数错误'
        return JsonResponse(data)
    type_id = int(type_id)
    result = UserFollowRel.objects.filter(id=type_id, use=user_id).count()
    if result:
        data['code'] = 4501
        data['msg'] = '已经关注,无需再次关注!'
        return JsonResponse(data)
    try:
        news_type = NewsType.objects.get(pk=type_id)
        userobj = User.objects.get(pk=user_id)
        uf_rel = UserFollowRel(id=news_type, use=userobj)
        uf_rel.save()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙,数据操作失败.'
        return JsonResponse(data)
    data['code'] = 200
    data['msg'] = '请求成功!'
    return JsonResponse(data)


@require_http_methods(['DELETE'])
@is_login_api
def remove_follow_type(request, type_id):
    data = {}
    user_id = request.session['user_id']
    uf_rel = UserFollowRel.objects.filter(id=type_id, use=user_id)
    if not uf_rel:
        data['code'] = 4601
        data['msg'] = '用户未关注,取消关注失败!'
        return JsonResponse(data)
    try:
        uf_rel.delete()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙,数据操作失败.'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)


def get_news_with_follow(request):
    data = {}
    user_id = request.session.get('user_id', None)
    try:
        if not user_id:
            news_set = NewsArticle.objects.all()[:30]
        else:
            user = User.objects.get(pk=user_id)
            follow_set = user.follow_type.all()
            follow_list = [x.id for x in follow_set]
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
            'publish_time': news.publish_time.strftime('%Y-%m-%d')
        }
        news_list.append(item)
    data['code'] = 200
    data['msg'] = '请求成功'
    data['news_list'] = news_list
    return JsonResponse(data)
