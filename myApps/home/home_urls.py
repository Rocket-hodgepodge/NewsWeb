"""
前端路由文件
AUTH: TTC
DATE: 2018年7月6日 01:47:45
"""

from django.urls import path

from myApps.home import home_views

urlpatterns = [
    path('', home_views.index),
    path('hotNews/', home_views.hot_news),
    path('news/', home_views.news),
    path('newsSearch/', home_views.news_search),
    # showNews 可加新闻ID参数
    path('showNews/<int:news_id>/', home_views.show_news),
    path('userInfo/', home_views.user_info),
    path('typeCount/', home_views.get_type_count),
    path('newsType/<int:type_id>/', home_views.news_type),
]
