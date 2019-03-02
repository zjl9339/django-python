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

def treeJson(request):
    data = [{
            "id": 1,
            "text": "主页",
            "state": "open",
            # "iconCls": "icon-save",
            "children": [{
                "id": 11,
                "text": "index",
                "attributes":{
                     "url": "/index"
                 },
            },{
                "id": 12,
                "text": "author",
                "attributes": {
                    "url": "/author/"
                },
            },{
                "id": 13,
                "text": "depart",
                "attributes": {
                    "url": "/depart/"
                },
            },{
                "id": 14,
                "text": "blog",
                "attributes": {
                    "url": "/blog/"
                },
            },{
                "id": 15,
                "text": "book",
                "attributes": {
                    "url": "/book/"
                },
            },{
                "id": 16,
                "text": "publisher",
                "attributes": {
                    "url": "/publisher/"
                },
            }
            ]
        },{
            "id": 2,
            "text": "Node 2",
            "state": "closed",
            "children": [{
                "id": 11,
                "text": "index",
                "attributes": {
                    "url": "/"
                },
            }]
        }]
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')