# -*-  coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .forms import AddForm
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
from proApp import models

def index(request):
    return render(request,"depart.html")

def showTreeDepart(request):
    list = models.Department.objects.all()
    departList = []
    for li in list:
        departList.append({
            "id": li.id,
            "name": li.name,
        })
    return HttpResponse(json.dumps(departList), content_type='application/json; charset=utf-8')

def getDepart(request):
    if request.method == "GET":
        list = models.Department.objects.all()
        departList = []
        for li in list:
            departList.append({
                "id": li.id,
                "name": li.name,
                # "publish_date": li.publish_date,
            })

        # 将int类型使用dumps()方法转为str类型
        depart_len = json.dumps(len(departList))
        # 构造一个字典
        json_data_list = {
            'ret': {
                'success': True,
                'retCode': 200,
                'retMsg': "Department查询成功！"
            },
            'rows': departList,
            'total': depart_len
        }
        return HttpResponse(json.dumps(json_data_list), content_type='application/json; charset=utf-8')

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        publish_date = request.POST.get("publish_date")
        update_time = request.POST.get("update_time")
        # 定一个字典用于保存前端发送过来的查询条件
        search_dict = dict()
        if publish_date:
            search_sql = models.Department.objects.filter(publish_date__gte=publish_date)
        else:
            search_sql = models.Department.objects

        if update_time:
            search_sql = search_sql.filter(publish_date__lte=update_time)

        # 序列化
        search_sql = search_sql.filter(title__contains=title).filter(content__contains=content)
        articleList = serializers.serialize("json", search_sql, ensure_ascii=False)
        articleList = json.loads(articleList)
        data = {
            'ret': {
                'success': True,
                'retCode': 200,
                'retMsg': "Department查询成功！"
            },
            'list': articleList
        }
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

def addDepart(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    department = request.POST.get("department")
    pthone = request.POST.get("pthone")
    dic = {
        'name': name,
        'email': email,
        'sex': sex,
        'department': department,
        'pthone': pthone,
    }
    models.Department.objects.create(**dic)
    ret = {
        'success': True,
        'retCode': 200,
        'retMsg': "Department添加成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def delDepart(request):
    id = request.POST.get("id")
    models.Department.objects.filter(id=id).delete()
    ret = {
        'success': True,
        'retCode': 200,
        'retMsg': "Department删除成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def modifyDepart(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    department = request.POST.get("department")
    pthone = request.POST.get("pthone")
    models.Department.objects.filter(id=id).update(name=name, email=email, sex=sex, department=department, pthone=pthone)
    ret = {
        'success': True,
        'retCode': 200,
        'retMsg': "Department修改成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

