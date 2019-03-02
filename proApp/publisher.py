# -*-  coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json
from proApp import models, base
from proApp.common import DateEncoder, Datagrid

@base.checkLogin
def index(request):
    return render(request,"publisher.html")

def getPublisher(request):
    if request.method == "GET":
        page = int(request.GET.get('page',0))-1
        rows = int(request.GET.get('rows',0))
        list = models.Publisher.objects.all().order_by("-id")
        allList = []
        for li in list:
            allList.append({
                "id": li.id,
                "name": li.name,
            })
        if page < 0 or rows == 0:
            json_data_list = allList
        else:
            total = len(allList)
            p = Datagrid()
            json_data_list = p.page(page, rows, total, allList)

        return HttpResponse(json.dumps(json_data_list), content_type='application/json; charset=utf-8')

    if request.method == "POST":
        page = int(request.POST.get('page', '')) - 1
        rows = int(request.POST.get('rows', ''))
        name = request.POST.get("name", '')
        sex = request.POST.get("sex")
        depart = request.POST.get("depart")
        dateFrom = request.POST.get("dateFrom")
        dateTo = request.POST.get("dateTo")
        # 定一个字典用于保存前端发送过来的查询条件
        search_dict = dict()
        if dateFrom:
            search_sql = models.Publisher.objects.filter(publish_date__gte=dateFrom)
        else:
            search_sql = models.Publisher.objects

        if dateTo:
            search_sql = search_sql.filter(publish_date__lte=dateTo)

        if int(sex)>-1:
            search_sql = search_sql.filter(sex__contains=sex)

        if (depart and int(depart)>-1):
            search_sql = search_sql.filter(depart=depart)

        # 序列化
        list = search_sql.filter(name__contains=name).order_by("-id")
        allList = []
        for li in list:
            allList.append({
                "id": li.id,
                "name": li.name,
                "email": li.email,
                "sex": li.sex,
                "depart": li.depart_id,
                "phone": li.phone,
                "account": li.account,
                "publish_date": json.loads(json.dumps(li.publish_date, cls=DateEncoder)),
            })
        total = len(allList)
        p = Datagrid()
        json_data_list = p.page(page, rows, total, allList)
        return HttpResponse(json.dumps(json_data_list), content_type='application/json; charset=utf-8')

def addPublisher(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    depart = models.Department.objects.get(pk=request.POST.get("depart"))
    phone = request.POST.get("phone")
    account = request.POST.get("account")
    dic = {
        'name': name,
        'email': email,
        'sex': sex,
        'depart': depart,
        'phone': phone,
        'account': account
    }
    models.Publisher.objects.create(**dic)
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "Author添加成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def delPublisher(request):
    id = request.POST.get("id")
    models.Publisher.objects.filter(id=id).delete()
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "Author删除成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def modifyPublisher(request):
    id = request.POST.get("modifyId")
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    depart = models.Department.objects.get(pk=request.POST.get("depart"))
    phone = request.POST.get("phone")
    account = request.POST.get("account")
    # publish_date = models.DateTimeField(u'发布时间', auto_now_add=True, editable=True, null=True, blank=True)
    models.Publisher.objects.filter(id=id).update(name=name, email=email, sex=sex, depart=depart, phone=phone, account=account )
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "Author修改成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

