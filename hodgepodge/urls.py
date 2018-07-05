"""hodgepodge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin_page/', include('myApps.admin.admin_page.admin_page_api_urls')),
    path('user_operation/', include('myApps.admin.user_operation.user_operation_api_urls')),
    path('user_permission/', include('myApps.admin.user_permission.user_permission_api_urls')),
    path('home_page/', include('myApps.home.home_page.home_page_api_urls')),
    path('news/', include('myApps.home.news.news_api_urls')),
    path('review/', include('myApps.home.review.review_operation_api_urls')),
    path('count/', include('count.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
