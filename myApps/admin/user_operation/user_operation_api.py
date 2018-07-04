"""
用户的登录注册接口
AUTH:
DATA:
"""
from io import BytesIO

from django.shortcuts import render
from django.http.response import HttpResponse
from myApps.untils.verify_code import VerifyCode


def hello_user_operation(request):
    return HttpResponse('Hello User Operation')


def get_verify_code(request):
    vcode = VerifyCode()
    image = vcode.verify_image
    request.session['verify_code'] = vcode.verify_code
    f = BytesIO()
    image.save(f, 'jpeg')
    resp = HttpResponse(f.getvalue(), content_type="image/jpeg")
    return resp
