# -*-  coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json,os,time
from proApp import models, base
from proApp.common import DateEncoder, Datagrid, utils
import logging
logger = logging.getLogger('django')

@base.checkLogin
def index(request):
    return render(request,"author.html")

def getAuthor(request):
    if request.method == "GET":
        page = int(request.GET.get('page',0))-1
        rows = int(request.GET.get('rows',0))
        list = models.Author.objects.all().order_by("-id")
        allList = []
        for li in list:
            allList.append({
                "id": li.id,
                "head_img": str(li.head_img),
                "name": li.name,
                "email": li.email,
                "sex": li.sex,
                "depart": li.depart_id,
                "phone": li.phone,
                "account": li.account,
                "publish_date": json.loads(json.dumps(li.publish_date, cls=DateEncoder)),
            })
        total = len(allList)
        if page < 0 or rows == 0:
            json_data_list = allList
        else:
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
            search_sql = models.Author.objects.filter(publish_date__gte=dateFrom)
        else:
            search_sql = models.Author.objects

        if name:
            search_sql = search_sql.filter(name=name)

        if dateTo:
            search_sql = search_sql.filter(publish_date__lte=dateTo)

        if int(sex)>-1:
            search_sql = search_sql.filter(sex__contains=sex)

        if (depart and int(depart)>-1):
            search_sql = search_sql.filter(depart=depart)

        # 序列化
        list = search_sql.order_by("-id")

        allList = []
        for li in list:
            allList.append({
                "id": li.id,
                "head_img": str(li.head_img),
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

def addAuthor(request):
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
    if request.FILES.get("headimg"):
        sql = models.Author
        head_img = utils.headimgHandle(request, request.FILES.get("headimg"), sql, None)
        dic['head_img'] = head_img
    models.Author.objects.create(**dic)
    utils.sendEmialHtml(request)
    ret = {
        'success': True,
        'retCode': 200,
        'retMsg': "Author添加成功！"
    }

    return HttpResponse(json.dumps(ret), content_type='application/json')

def delAuthor(request):
    id = request.POST.get("id")
    models.Author.objects.filter(id=id).delete()
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "Author删除成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def modifyAuthor(request):
    id = request.POST.get("modifyId")
    sql = models.Author
    name = request.POST.get("name")
    email = request.POST.get("email")
    sex = request.POST.get("sex")
    depart = models.Department.objects.get(pk=request.POST.get("depart"))
    phone = request.POST.get("phone")
    account = request.POST.get("account")
    # publish_date = models.DateTimeField(u'发布时间', auto_now_add=True, editable=True, null=True, blank=True)
    if request.FILES.get("headimg"):
        head_img = utils.headimgHandle(request, request.FILES.get("headimg"), sql, id)
        models.Author.objects.filter(id=id).update(head_img=head_img, name=name, email=email, sex=sex, depart=depart,
                                                   phone=phone, account=account)
    else:
        models.Author.objects.filter(id=id).update(name=name, email=email, sex=sex, depart=depart,
                                                   phone=phone, account=account)


    ret = {
        'success': True,
        'retCode': 200,
        'retMsg': "Author修改成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def uploadHeadimg(request):
    authorId = request.GET.get("id")
    user = request.user
    if request.method == "POST":
        ret = {}
        try:
            # 拿文件数据
            icon = request.FILES.get('headimg')
            # 获取图片的随机名
            file_name =  '%s.jpg' % str(int(time.time()))
            # 拼接一个自己的文件路径
            image_path = os.path.join('media/icons/', file_name)
            # 打开拼接的文件路径
            with open(image_path, 'wb')as fp:
                # 遍历图片的块数据（切块的传图片）
                for i in icon.chunks():
                    # 将图片数据写入自己的那个文件
                    fp.write(i)
            # 拼接返回数据
            ret = {
                'success': True,
                'retCode': 200,
                'retMsg': "上传成功！"
            }
        except Exception as e:
            logger.error("author头像上传失败" + str(e))
            ret = {
                'success': False,
                'retCode': 500,
                'retMsg': "上传失败！"+str(e)
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')
