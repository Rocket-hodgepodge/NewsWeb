"""
评论/点赞 模块
AUTH: Y.win
DATE: 2018/7/4
"""
import json

from myApps.models import Review
from django.http.response import HttpResponse


def add_review(request):
    """添加评论"""
    if request.method == 'POST':
        # 获取 用户id/新闻id/评论内容
        user_id = request.session['user_id']
        news_id = request.POST.get('news_id')
        rev_content = request.POST.get('review')
        # 设置返回数据
        data = {
            'code': 200
        }
        try:
            Review.objects.create(
                Use_id=user_id,
                News_id=news_id,
                Rev_content=rev_content
            )
            Review.save()
            return HttpResponse(json.dumps(data))
        except Exception as e:

            return HttpResponse(json.dumps())
        return
