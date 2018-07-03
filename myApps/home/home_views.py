from django.shortcuts import render
from django.http.response import HttpResponse
from myApps.models import User


def hello_world(request):
    return HttpResponse('hello world!')
