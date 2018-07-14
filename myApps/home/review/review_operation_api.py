"""
评论/点赞 模块
AUTH: TTC
DATE: 2018/7/4
"""
from django import db
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from myApps.models import Review, ReviewLiked, User
from django.http.response import JsonResponse

from myApps.untils.wrapper_set import is_login_api


@require_POST
@is_login_api
def add_review(request, user_id):
    data = {}
    # user_id = request.session.get('user_id')
    news_id = request.POST.get('news_id', None)
    rev_content = request.POST.get('review', None)
    if not news_id or not rev_content:
        data['code'] = 504
        data['msg'] = '参数错误'
        return JsonResponse(data)
    try:
        Review(use_id=user_id, news_id=news_id, rev_content=rev_content).save()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙， 请稍后再试！'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)


@require_GET
def get_review(request):
    data = {}
    news_id = request.GET.get('news_id', None)
    user_id = request.GET.get('user_id', None)
    page = request.GET.get('page', 1)
    rows = request.GET.get('rows', 2)
    q1 = Q(news_id=news_id) if news_id else None
    q2 = Q(user_id=user_id) if user_id else None
    try:
        if q1 and q2:
            review_set = Review.objects.filter(q1 & q2)
        elif q1:
            review_set = Review.objects.filter(q1)
        elif q2:
            review_set = Review.objects.filter(q2)
        else:
            review_set = Review.objects.all()
        total = review_set.count()
        if page and rows:
            page = int(page)
            rows = int(rows)
            review_set = review_set.order_by('-create_time')[(page - 1) * rows: page * rows]
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后再试！'
        return JsonResponse(data)
    review_list = []
    for review_obj in review_set:
        item = {
            'id': review_obj.id,
            'news_id': review_obj.news_id,
            'user_id': review_obj.use_id,
            'liked_num': review_obj.reviewliked_set.filter(is_liked=True).count(),
            'unliked_num': review_obj.reviewliked_set.filter(is_liked=False).count(),
            'user_name': review_obj.use.nick_name,
            'time': review_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'rev_content': review_obj.rev_content
        }
        review_list.append(item)
    data['code'] = 200
    data['msg'] = '请求成功'
    data['total'] = total if total else 0
    data['rows'] = review_list
    return JsonResponse(data)


@require_http_methods(['DELETE'])
def delete_review(request, review_id):
    data = {}
    try:
        Review.objects.get(pk=review_id).delete()
    except ObjectDoesNotExist:
        data['code'] = 5401
        data['msg'] = '评论ID不存在'
        return JsonResponse(data)
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后重试！'
        return JsonResponse(data)
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)


@require_POST
@is_login_api
def add_liked_review(request, user_id):
    # user_id = request.session.get('user_id')
    data = {}
    review_id = request.POST.get('r_id', None)
    is_like = int(request.POST.get('is_liked', 1))
    is_like = True if is_like else False
    if not review_id:
        data['code'] = 504
        data['msg'] = '请求参数错误'
        return JsonResponse(data)
    try:
        is_action = ReviewLiked.objects.filter(r_id=review_id, use_id=user_id).count()
        if is_action:
            data['code'] = 5301
            data['msg'] = '无需重复点击'
            return JsonResponse(data)
        review_obj = Review.objects.get(pk=review_id)
        ReviewLiked(r_id=review_obj, use_id=user_id, is_liked=is_like).save()
    except db.Error:
        data['code'] = 400
        data['msg'] = '服务器忙，请稍后再试'
        return JsonResponse(data)
    except ObjectDoesNotExist:
        data['code'] = 5302
        data['msg'] = '用户或评论不存在！'
    else:
        data['code'] = 200
        data['msg'] = '请求成功'
        return JsonResponse(data)

