# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# ajax get
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse( "sum = "+ str(c))

# ajax post
def add2(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))