from django.urls import path

from myApps.home.news import news_liked_api, news_operation_api, news_follow_api

urlpatterns = [
    path('', news_operation_api.hello_news_operation),
    path('liked/', news_liked_api.hello_news_liked),
    path('news_liked/', news_liked_api.news_liked),  # 测试用
    path('news_liked_num/', news_liked_api.get_news_liked_num),  # 测试用
    path('news_search/', news_operation_api.news_title_search),  # 测试用
    path('news_type/', news_operation_api.news_type_search),  # 测试用

    path('newsSearch/', news_operation_api.news_title_search),
    path('alterNews/', news_operation_api.alter_news),

    path('query/', news_operation_api.integrated_query),
    path('all_type/', news_operation_api.news_all_type),
    path('delNews/<int:news_id>/', news_operation_api.del_news),
    path('getOneNews/<int:news_id>/', news_operation_api.get_one_news),
    path('addFollow/', news_follow_api.add_follow_type),
    path('rmFollow/<int:type_id>/', news_follow_api.remove_follow_type),
    path('getFollowNews/', news_follow_api.get_news_with_follow),
    path('getNewsOrder/', news_operation_api.get_news_order),
]
