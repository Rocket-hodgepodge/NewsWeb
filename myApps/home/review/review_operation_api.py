"""
评论/点赞 模块
AUTH: Y.win
DATE: 2018/7/4
"""
import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from myApps.models import Review, User, ReviewLiked
from django.http.response import JsonResponse


def add_review(request):
    """添加评论"""
    if request.method == 'POST':
        # 获取 用户id
        data = {}
        user_id = request.session.get('user_id', None)
        # 验证用户是否登录, 未登陆返回 用户未登录
        if not user_id:
            data['code'] = 5101
            data['msg'] = '用户未登陆'
            return JsonResponse(data)
        # 获取用户权限
        rol_id = User.objects.get(id=user_id).rol_id
        if rol_id != 2:
            data['code'] = 501
            data['msg'] = '用户没有权限'
            return JsonResponse(data)
        news_id = request.POST.get('news_id')
        rev_content = request.POST.get('review')
        # 设置返回数据
        if len(rev_content) > 125:
            data['code'] = 5102
            data['msg'] = '评论字数超过125,添加失败'
            return JsonResponse(data)
        try:
            # 向数据库添加评论
            review = Review.objects.create(
                Use_id=user_id,
                News_id=news_id,
                Rev_content=rev_content
            )
            review.save()
            data['code'] = 200
            return JsonResponse(data)
        except Exception as e:
            data['code'] = 400
            data['msg'] = '数据库访问失败'
            return JsonResponse(data)


def get_review(request):
    """评论分页展示"""
    if request.method == 'GET':
        data = {}
        args = request.GET
        news_id = args.get('news_id')  # 新闻id
        page = args.get('page')  # 页码
        rows = args.get('rows')  # 每页评论数量
        try:
            # 获取某条新闻的所有评论对象
            all_rev_objects = Review.objects.all(news=news_id)
        except Exception as e:
            # 如果数据库连接错误, 则返回
            data['code'] = 400
            data['msg'] = '数据库访问失败'
            return JsonResponse(data)
        # 如果某条新闻有评论，就将评论对象分页
        if all_rev_objects:
            paginator = Paginator(all_rev_objects, rows)
            page_nums = paginator.num_pages
            # 获取分页的评论对象, 如果page
            try:
                page_rev_objects = paginator.page(page)
            except EmptyPage:
                page_rev_objects = paginator.page(1)
            except InvalidPage:
                page_rev_objects = paginator.page(page_nums)
        else:
            # 如果没有评论 就返回空
            page_rev_objects = None
        data['data'] = []
        data['code'] = 200
        # 返回评论id, 评论内容, 用户名, 用户id, 评论点赞数, 评论点踩数
        for rev_object in page_rev_objects:
            user_name = rev_object.use.name
            is_liked = rev_object.reviewliked_set
            # 查找评论的赞和踩, 如果没有则将值设为0
            like = is_liked.filter(is_liked=1)
            dislike = is_liked.filter(is_liked=0)
            if like:
                like_num = len(like)
            else:
                like_num = 0
            if dislike:
                dislike_num = len(dislike)
            else:
                dislike_num = 0
            rev_msg = (rev_object.id, rev_object.rev_content,
                       user_name, rev_object.id, like_num, dislike_num)
            data['data'].append(rev_msg)

        return JsonResponse(data)


def is_like(request):
    """返回评论的点赞与点踩数"""
    if request.method == 'GET':
        args = request.GET
        rev_id = args.get('review_id')  # 获取评论id
        data = {}
        try:
            is_like_objects = ReviewLiked.objects.fileter(id=rev_id)
            like_objects = is_like_objects.filter(is_liked=1)
            dislike_objects = is_like_objects.filter(is_liked=0)
        except Exception as e:
            data['code'] = 400
            data['msg'] = '数据库访问失败'
            return JsonResponse(data)
        # 获取点赞和点踩的数量, 如果没有就设为零
        if like_objects:
            like_num = len(like_objects)
        else:
            like_num = 0
        if dislike_objects:
            dislike_num = len(dislike_objects)
        else:
            dislike_num = 0
        # 点赞数量和点踩数量
        data['code'] = 200
        data['msg'] = (like_num, dislike_num)
        return JsonResponse(data)


def add_is_liked(request):
    """添加点赞或者点踩"""
    if request.method == "POST":
        request.POST.get()