from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .forms import AddForm
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from proApp import models, article, base

# Create your views here.
@base.checkLogin
def index(request):
    dict = {
        "article_list": article.getArticle(),
    }
    return render(request, 'index.html',dict)


def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    List = map(str, range(10))  # 一个长度为10的 List
    athlete_list = {}
    score = 90
    form = {}
    dict = {
        'string': string,
        'TutorialList':TutorialList,
        'info_dict':info_dict,
        'List':List,
        'athlete_list':athlete_list,
        'score':score,
        'form': form,
    }
    return render(request,"home.html",dict)

def old_add2_redirect(request, a, b):
    return HttpResponse(
        reverse('add2', args=(a, b))
    )

#  传递一个数组或字典到网页，由JS处理，再显示出来。
def ajax_list(request):
    a = list(range(100))
    return HttpResponse(json.dumps(a), content_type='application/json')


def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django','name':"翟娟丽"}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

from .models import BioDrug
@csrf_exempt
def select_drug(request):
    if request.method == 'POST':
        drugs_id = request.POST.get('drugs')
        drugs_id_list = drugs_id.strip().split(' ')
        return HttpResponse(','.join(drugs_id_list))
    else:
        drugs = BioDrug.objects.filter(inputer__isnull=True)
        return render(request,'home.html',{'drugs': drugs})


# login/loginout
def login(request):
    loginDict = {

    }
    return render(request, 'login.html',loginDict)

#  操作数据库  增删改查、连表功能
# def showArticle():
#     article_list = models.Article.objects.all()
#     return article_list

# 默认访问页面
def ajax_index(request):
    return render(request, 'ajax_index.html')

# Ajax POST 提交数据
def ajax_post(request):
    return HttpResponse('')


# Ajax 返回 JSON 数据
def ajax_json(request):
    return HttpResponse('')

def showUser(request):
    from proApp import models
    user_list = models.Person.objects.all()
    user_list = [
        {'name': 'Django', 'age': 18, 'phone': '13500000000'}
    ]
    return HttpResponse(json.dumps(user_list), content_type='application/json')