from django import db
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from myApps.models import User, UserFollowRel, NewsType
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
