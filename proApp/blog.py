# -*-  coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json
from proApp import models
from proApp.common import DateEncoder,Datagrid

def index(request):
    return render(request,"blog.html")