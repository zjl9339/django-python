"""djangoPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import module
from proApp import views as proApp_views
from proApp import base as proApp_base
from proApp import common as proApp_common
from proApp import article as proApp_article
from proApp import add as proApp_add
from proApp import add2 as proApp_add2
from proApp import author as proApp_author
from proApp import depart as proApp_depart
from proApp import tree as proApp_tree
from proApp import blog as proApp_blog
from proApp import login as proApp_login
from proApp import book as proApp_book
from proApp import publisher as proApp_publisher

from django.views.static import serve
from django.conf import settings

pageurlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('', proApp_views.index, name="index"),
    path('index/', proApp_views.index, name="index"),
    path('login/', proApp_views.login, name="login"),
    path('home/', proApp_views.home, name="home"),
    path('module/', module.hello, name="module"),
    path('author/', proApp_author.index, name="author"),
    path('depart/', proApp_depart.index, name="depart"),
    path('blog/', proApp_blog.index, name="blog"),
    path('book/', proApp_book.index, name="book"),
    path('publisher/', proApp_publisher.index, name="publisher"),
]
interfaceurlpatterns = [
    path('add/', proApp_add.add,name='add'),
    path('new_add/<int:a>/<int:b>', proApp_add.add2,name='add2'),
    path('ajax_list/', proApp_views.ajax_list, name='ajax_list'),
    path('ajax_dict/', proApp_views.ajax_dict, name='ajax_dict'),
    path('select_drug/', proApp_views.select_drug, name='select_drug'),
    path('getArticle/', proApp_article.getArticle, name='showArticle'), # Article start
    path('addArticle/', proApp_article.addArticle, name='addArticle'),
    path('delArticle/', proApp_article.delArticle, name='delArticle'),
    path('modifyArticle/', proApp_article.modifyArticle, name='modifyArticle'),
    path('searchArticle/', proApp_article.searchArticle, name='searchArticle'), # Article end
    path('getAuthor/', proApp_author.getAuthor, name='getAuthor'),     # Author start
    path('delAuthor/', proApp_author.delAuthor, name='delAuthor'),
    path('addAuthor/', proApp_author.addAuthor, name='addAuthor'),
    path('modifyAuthor/', proApp_author.modifyAuthor, name='modifyAuthor'),
    path('uploadHeadimg/', proApp_author.uploadHeadimg, name='uploadHeadimg'),  # author头像上传 Author end
    path('getDepart/', proApp_depart.getDepart, name='getDepart'),     # Depart start
    path('showTreeDepart/', proApp_depart.showTreeDepart, name='showTreeDepart'),     # Depart start
    path('delDepart/', proApp_depart.delDepart, name='delDepart'),
    path('addDepart/', proApp_depart.addDepart, name='addDepart'),
    path('modifyDepart/', proApp_depart.modifyDepart, name='modifyDepart'), # Depart end
    path('user/', proApp_views.showUser, name='showUser'),
    path('ajax_index/', proApp_views.ajax_index, name='ajax_index'),
    path('ajax_post/', proApp_views.ajax_post, name='ajax_post'),
    path('ajax_json/', proApp_views.ajax_json, name='ajax_json'),
    path('treeJson/', proApp_tree.treeJson, name='treeJson'),
    path('loginIn/', proApp_login.loginIn, name='loginIn'),
    path('loginOut/', proApp_base.loginOut, name='loginOut'),
    path('getCaptcha/', proApp_login.getCaptcha, name='getCaptcha'),
    path('modifyPsd/', proApp_base.modifyPsd, name='modifyPsd'),
    path('getBook/', proApp_book.getBook, name='getBook'),                        # book
    path('addBook/', proApp_book.addBook, name='addBook'),
    path('delBook/', proApp_book.delBook, name='delBook'),
    path('modifyBook/', proApp_book.modifyBook, name='modifyBook'),               # book
    path('getPublisher/', proApp_publisher.getPublisher, name='getPublisher'),    # 出版社
    path('addPublisher/', proApp_publisher.addPublisher, name='addPublisher'),
    path('delPublisher/', proApp_publisher.delPublisher, name='delPublisher'),
    path('modifyPublisher/', proApp_publisher.modifyPublisher, name='modifyPublisher'), # 出版社
    path('exportBookExcel/', proApp_book.exportBookExcel, name='exportBookExcel'),   # 导出功能
    path('importBook/', proApp_book.importBook, name='importBook'),   # 导入功能
    path('uploadFile/', proApp_book.uploadFile, name='uploadFile'),   # 单附件上传
    path('uploadMoreFile/', proApp_book.uploadMoreFile, name='uploadMoreFile'),   # 多附件上传
    path('uploadBookCover/', proApp_book.uploadBookCover, name='uploadBookCover'),   # 图书封面上传，图片上传

]

urlpatterns = pageurlpatterns + interfaceurlpatterns


#  定时任务1
from apscheduler.scheduler import Scheduler
import datetime, time
from proApp.task import tasks
sched = Scheduler()    # 创建调度器

@sched.interval_schedule(minutes= 100)
def my_task():
    task = tasks()
    task.testFuncton()

sched.start()


#  定时任务2  阻塞式：前一个执行完后面的才执行 单线程
import sched, time
schedule = sched.scheduler(time.time, time.sleep)
def print_time():
    print ("From print_time: ", time.time())
def func(string1,float1):
    print("定时任务2: now is",time.time()," | output=",string1,float1)

schedule.enter(5, 1, print_time, ())
schedule.enter(10, 1, print_time, ())
schedule.enter(2, 0, func, ("test1",time.time()))
schedule.run()

#  定时任务3  非阻塞式：多线程  可以同时执行
import time
from threading import Timer

def printTime(enter_time):
    print ("定时任务3: now is", time.time(), "enter_the_box_time is", enter_time)

Timer(5, printTime, (time.time(),)).start()
Timer(10, printTime, (time.time(),)).start()

#  固定时间执行某项任务
def doSth():
    print('test')
    # 假装做这件事情需要一分钟
    time.sleep(60)

def main(h=0, m=0, s=0):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            print (now.hour, now.minute, now.second)
            if now.hour==h and now.minute==m and now.second==s:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(20)
        # 做正事，一天做一次
        doSth()

main()




