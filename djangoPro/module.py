#!D:\anzhuang\python\python.exe
# -*-  coding:utf-8 -*-
import codecs, sys
import cgi, cgitb

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print("Content-type:text/html")
print()  # 空行，告诉服务器结束头部

# from django.http import HttpResponse
# def hello(request):
#     return HttpResponse("hello world")

from django.shortcuts import render
def hello(request):
    context = {}
    context['hello'] = 'module，python'
    return render(request,'module.html',context)

