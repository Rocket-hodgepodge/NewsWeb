from django.urls import path

from myApps.home.news import news_liked_api, news_operation_api

urlpatterns = [
    path('', news_operation_api.hello_news_operation),
    path('liked/', news_liked_api.hello_news_liked),
    path('news_search/', news_operation_api.news_title_search),  # 测试用
    path('news_type/', news_operation_api.news_type_search),  # 测试用
    path('newsSearch/', news_operation_api.news_search),
    path('query/', news_operation_api.integrated_query),
]
