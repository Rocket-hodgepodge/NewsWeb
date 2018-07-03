from django.shortcuts import render
from django.http.response import HttpResponse


def hello_news_operation(request):
    return HttpResponse('Hello News Operation')
