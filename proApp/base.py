# -*-  coding:utf-8 -*-
from django.contrib import auth
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
import datetime
from proApp import models
from django.views.decorators.csrf import csrf_exempt

def loginOut(request):
    auth.logout(request)
    return HttpResponse('/login')

def modifyPsd(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        models.Author.objects.filter(id=id).update(password=password)
        ret = {
            'success': True,
            'retCode': 200,
            'retMsg': "密码修改成功！"
        }
        return HttpResponse(json.dumps(ret), content_type='application/json')

#  装饰器
def checkLogin(func):
    """
    查看session值用来判断用户是否已经登录
    :param func:
    :return:
    """
    def warpper(request,*args,**kwargs):
        if request.session.get('username', False):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')

    return warpper


