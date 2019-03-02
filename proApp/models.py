# -*- coding:utf-8 -*-
import sys,os
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from django.db import models
from django import forms
from django.utils.html import format_html
import uuid

# Create your models here.
class Catinfo(models.Model):
    name = models.CharField(max_length=10,verbose_name = "名称")
    nameinfo = models.CharField(max_length=1000)
    feature = models.CharField(max_length=1000)
    livemethod = models.CharField(max_length=1000)
    feednn = models.CharField(max_length=1000)
    feedmethod = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Person(models.Model):
    sex_choice = (
        (0, '男'),
        (1, '女'),
    )
    name = models.CharField(max_length=30,verbose_name = "姓名")
    age = models.IntegerField()
    sex = models.IntegerField(choices=sex_choice, default=0)
    publish_date = models.DateTimeField(u'更新时间', auto_now_add=True, editable=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '人员管理'


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def headimgPath(instance, filename):  # instance  当前这条数据
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join('media/icons', filename)    # return the whole path to the file

class Author(models.Model):
    sex_choice = (
        (0, u'男'),
        (1, u'女'),
    )
    head_img = models.ImageField(upload_to=headimgPath,default="")
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=50,default="")
    password = models.CharField(max_length=255,default="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
    email = models.EmailField()
    sex = models.IntegerField(choices=sex_choice,default=0)
    depart = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=255,default="1")
    book = models.ManyToManyField('Book',related_name='author_book')
    publish_date = models.DateTimeField(u'发布时间', auto_now_add=True, editable=True, null=True, blank=True)

    def colored_name(self):
        if self.name == 'zjl':
            color_code = "green"
        else:
            color_code = "red"
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            color_code,
            self.name,
        )
    colored_name.short_description = u"性别"

    def image_show(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.head_img,
        )


    def __str__(self):
        return self.name

def bookCoverPath(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join(instance.user.id, "img", filename)    # return the whole path to the file

class Book(models.Model):
    id = models.FloatField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=1)
    saleNum = models.IntegerField(default=1)
    publisher = models.ForeignKey(Publisher,on_delete=models.DO_NOTHING)
    author = models.ManyToManyField(Author,related_name='book_author')
    publish_date = models.DateTimeField(u'发布时间', auto_now_add=True, editable=True, null=True, blank=True)
    bookCover = models.ImageField(upload_to=bookCoverPath) #,height_field='url_height', width_field='url_width',processors=[ResizeToFill(85,85)] #图像尺寸处理
    # fileOnly = models.FileField(upload_to='files',default="")
    fileMore = models.FileField(upload_to='files/%Y%m%d',default="")

    def author_list(self):
        return ','.join([i.name for i in self.author.all()])

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.DO_NOTHING,)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline

class Article(models.Model):
    title = models.CharField(u'标题', max_length=256)
    content = models.TextField(u'内容')

    publish_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title

class BioDrug(models.Model):
    name = models.CharField(max_length=100)
    inputer = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.DO_NOTHING,)

    create_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return self.name