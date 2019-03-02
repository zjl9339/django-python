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

def getArticle():
    article_list = models.Article.objects.all()
    return article_list

def searchArticle(request):
    if request.method == "GET":
        article_list = models.Article.objects.all()
        return article_list

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        publish_date = request.POST.get("publish_date")
        update_time = request.POST.get("update_time")
        # 定一个字典用于保存前端发送过来的查询条件
        search_dict = dict()
        if publish_date:
            search_sql = models.Article.objects.filter(publish_date__gte=publish_date)
        else:
            search_sql = models.Article.objects

        if update_time:
            search_sql = search_sql.filter(publish_date__lte=update_time)

        # 序列化
        search_sql = search_sql.filter(title__contains=title).filter(content__contains=content)  # 包含模糊匹配
        articleList = serializers.serialize("json", search_sql, ensure_ascii=False)
        # 字符串转字典
        articleList = json.loads(articleList)
        data = {
            'ret': {
                'success': True,
                'retCode': 200,
                'retMsg': "文章查询成功！"
            },
            'list': articleList
        }
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def addArticle(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    dic = {'title': title, 'content': content}
    models.Article.objects.create(**dic)
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "文章添加成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def delArticle(request):
    id = request.POST.get("id")
    models.Article.objects.filter(id = id).delete()
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "文章删除成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

def modifyArticle(request):
    id = request.POST.get("id")
    title = request.POST.get("title")
    content = request.POST.get("content")
    models.Article.objects.filter(id=id).update(title=title, content=content)
    ret = {
        'success': True,
        'retCode': 0,
        'retMsg': "文章修改成功！"
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')

