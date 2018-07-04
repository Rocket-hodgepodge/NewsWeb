"""
用户的登录注册接口
AUTH:
DATA:
"""
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from io import BytesIO

from myApps.untils import verify_code
from myApps.models import User, Role


def hello_user_operation(request):
    return HttpResponse('Hello User Operation')


def register(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html')
    if request.method == 'POST':
        data = {}
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            v_code = request.POST.get('v_code')
        except KeyError as e:
            data['code'] = 505
            data['msg'] = '请求参数错误' + str(e)
            return JsonResponse(data)

        if v_code != request.session['v_code']:
            data['code'] = 3004
            data['msg'] = '注册验证码不正确'
            return JsonResponse(data)
        if password != re_password:
            data['code'] = 3005
            data['msg'] = '两次密码不一致'
            return JsonResponse(data)
        if User.objects.filter(name=username).first():
            data['code'] = 3001
            data['msg'] = '用户名已存在'
            return JsonResponse(data)
        password = make_password(password)
        nick_name = username + str(datetime.now())
        last_login_time = datetime.now()
        try:
            user_dict = {'rol': Role.objects.get(id=2), 'name': username, 'password': password,
                         'nick_name': nick_name, 'last_login_time': last_login_time}
            User.objects.create(**user_dict)
            data['code'] = 200
            data['msg'] = '注册成功'
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,数据操作失败'
            return JsonResponse(data)


def login(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html')
    if request.method == 'POST':
        data = {}
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            v_code = request.POST.get('v_code')
        except KeyError as e:
            data['code'] = 505
            data['msg'] = '请求参数错误' + str(e)
            return JsonResponse(data)

        if v_code != request.session['v_code']:
            data['code'] = 3203
            data['msg'] = '登陆验证码错误'
            return JsonResponse(data)
        try:
            user = User.objects.filter(name=username).first()
            if not user:
                data['code'] = 3201
                data['msg'] = '用户不存在'
                return JsonResponse(data)
            if not check_password(password, user.password):
                data['code'] = 3202
                data['msg'] = '密码错误'
                return JsonResponse(data)
            request.session['user_id'] = user.id
            request.session['role_id'] = user.rol_id
            data['code'] = 200
            data['msg'] = '登录成功'
            data['role_id'] = user.rol_id
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data['code'] = 400
            data['msg'] = '服务器忙,请求失败'
            return JsonResponse(data)


def set_verify(request, v_random):
    print(v_random)
    if request.method == 'GET':
        v_code = verify_code.VerifyCode()
        image = v_code.verify_image
        f = BytesIO()
        image.save(f, 'jpeg')
        resp = HttpResponse(f.getvalue(), content_type='image/jpeg')
        request.session['v_code'] = v_code.verify_code
        return resp
