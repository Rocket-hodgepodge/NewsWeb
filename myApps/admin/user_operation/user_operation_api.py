"""
用户的登录注册接口
AUTH:
DATA:
"""
import uuid
from datetime import datetime
import os

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from io import BytesIO
import qiniu
from PIL import Image

from hodgepodge.settings import BASE_DIR
from myApps.untils import verify_code
from myApps.models import User, Role


def hello_user_operation(request):
    return HttpResponse('hello')


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
            user.last_login_time = datetime.now()
            user.save()
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


def logout(request):
    if request.method == 'GET':
        for key in ['user_id', 'role_id']:
            del request.session[key]
        data = {'code': 200, 'msg': '注销成功'}
        return JsonResponse(data)


def icon_modify(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            file_ex = file.name.split('.')[-1]
            media_dir = os.path.join(os.path.join(BASE_DIR, 'static\media'), 'image.' + file_ex)
            with open(media_dir, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            access_key = 'rdNJE5t51H_Y8MDgF_Cg4d1q5fjVQvvR6dDgIHnY'
            secret_key = 'DBSZaWdYKsfqvRaAqvRkPpGtcD-XiLDmsYnFBIZj'
            bucket_url = 'pbfkv2zhm.bkt.clouddn.com'  # 仓库域名
            bucket_name = 'hodge'  # 仓库名
            image_name = uuid.uuid1()
            q = qiniu.Auth(access_key, secret_key)  # 验证
            token = q.upload_token(bucket_name, image_name)
            ret, info = qiniu.put_file(token, image_name, media_dir)
            path = 'http://{}/{}'.format(bucket_url, ret['key'])
            User.objects.filter(pk=request.session['user_id']).update(head_icon=path)
            data = {'code': 200, 'path': path}
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data = {'code': 400}
            return JsonResponse(data)


def info_modify(request):
    if request.method == 'GET':
        try:
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            data = {'code': 200, 'nick_name': user.nick_name, 'name': user.name, 'head_icon': user.head_icon,
                    'last_login_time': user.last_login_time.date()}
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data = {'code': 300, 'msg': '未登录'}
            return JsonResponse(data)
    if request.method == 'POST':
        nick_name = request.POST.get('nick_name')
        try:
            User.objects.filter(pk=request.session['user_id']).update(nick_name=nick_name)
            data = {'code': 200, 'msg': '操作成功'}
            return JsonResponse(data)
        except Exception as e:
            print(e)
            data = {'code': 400, 'msg': '服务器忙,数据操作失败'}
            return JsonResponse(data)
