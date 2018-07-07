from django.urls import path

from myApps.home.news import news_liked_api, news_operation_api

urlpatterns = [
    path('', news_operation_api.hello_news_operation),
    path('liked/', news_liked_api.hello_news_liked),
    path('get_news_liked_num/', news_liked_api.get_news_liked_num),
    path('news_liked/', news_liked_api.news_liked),
    path('news_search/', news_operation_api.news_title_search),  # 测试用
    path('news_type/', news_operation_api.news_type_search),  # 测试用
    path('newsSearch/', news_operation_api.news_search),
    path('query/', news_operation_api.integrated_query),
    path('del_news/', news_operation_api.del_news),
    path('alter_news/', news_operation_api.alter_news),
]
