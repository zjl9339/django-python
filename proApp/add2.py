# coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse(u"欢迎光临，python App 学习案例")

def add(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))