# -*-  coding:utf-8 -*-
from django.http import HttpResponse
import json, os
import datetime, time
from django.db import models
import logging
logger = logging.getLogger('django')
import uuid,hashlib  # 随机数使用
# 发送邮件
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# python自带的json，将数据转换为json数据时，datetime格式的数据报错. 所以重写构造json类，遇到日期特殊处理
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            print(e)

#  表格
class Datagrid():
    def __init__(self):
        self.rowPageList = []
        self.json_data_list = {}

    #  分页处理
    def page(self, page, rows, total, allList):  # page: 当前页码   rows：表格1页面表格行数  total：所有数据len,  allList：所有数据
        rowPageList = []
        json_data_list = {}
        try:
            if (page == 0):
                page = 1
                if (rows > len(allList)):
                    json_data_list = {
                        'ret': {
                            'success': True,
                            'retCode': 200,
                            'retMsg': "查询成功！"
                        },
                        'rows': allList,
                        'total': total
                    }
                else:
                    for s in range(page * rows):
                        rowPageList.append(allList[s])
                        json_data_list = {
                            'ret': {
                                'success': True,
                                'retCode': 200,
                                'retMsg': "查询成功！"
                            },
                            'rows': rowPageList,
                            'total': total
                        }
            else:
                ss = allList[page * rows:]
                if (len(ss) < rows):
                    json_data_list = {
                        'ret': {
                            'success': True,
                            'retCode': 200,
                            'retMsg': "查询成功！"
                        },
                        'rows': ss,
                        'total': total
                    }
                else:
                    for i in range(page * rows):
                        rowPageList.append(ss[i])
                        json_data_list = {
                            'ret': {
                                'success': True,
                                'retCode': 200,
                                'retMsg': "查询成功！"
                            },
                            'rows': rowPageList,
                            'total': total
                        }
            return json_data_list
        except Exception as e:
            logger.info('-------------------------')
            logger.error(str(e))
            logger.warn('warn')
            logger.debug('debug')

    # 数据删除
    def delate(self,request,Table,pkName,pkValue):
        pkValue = request.POST.get(pkValue)
        models.Table.objects.filter(pkName=pkValue).delete()
        ret = {
            'success': True,
            'retCode': 0,
            'retMsg': "删除成功！"
        }
        return ret


# def importBook2(request):
#     import time
#     import random
#     time1 = time.time()
#     f = open('C:\Users\24950\Downloads\test.xls')
#     print( u"读取文件结束,开始导入!")
#     time2 = time.time()
#     WorkList = []
#     next(f)  # 将文件标记移到下一行
#     y = 0
#     n = 1
#     for line in f:
#         row = line.replace('"', '')  # 将字典中的"替换空
#         row = row.split(';')  # 按;对字符串进行切片
#         y = y + 1
#         WorkList.append(models.Book(acct_month=row[0], serv_id=row[1], acc_nbr=row[2], user_name=row[3], acct_code=row[4],
#                                acct_name=row[5], product_name=row[6], current_charge=row[7], one_charge=row[8],
#                                two_charge=row[9], three_charge=row[10], four_charge=row[11], five_charge=row[12],
#                                six_charge=row[13], seven_charge=row[14], eight_charge=row[15], nine_charge=row[16],
#                                ten_charge=row[17], eleven_charge=row[18], twelve_charge=row[19], oneyear_charge=row[20],
#                                threeyear_charge=row[21], upthreeyear_charge=row[22], all_qf=row[23],
#                                morethree_qf=row[24],
#                                aging=row[25], serv_state_name=row[26], mkt_chnl_name=row[27], mkt_chnl_id=row[28],
#                                mkt_region_name=row[29], mkt_region_id=row[30], mkt_grid_name=row[31],
#                                mkt_grid_id=row[32],
#                                prod_addr=row[33]))
#         n = n + 1
#         if n % 50000 == 0:
#             print (n)
#             D072Qf.objects.bulk_create(WorkList)
#             WorkList = []
#             time3 = time.time()
#             print ("读取文件耗时" + str(time2 - time1) + "秒,导入数据耗时" + str(time3 - time2) + "秒!")
#     time3 = time.time()
#     print (n)
#     models.Book.objects.bulk_create(WorkList)
#     print ("读取文件耗时" + str(time2 - time1) + "秒,导入数据耗时" + str(time3 - time2) + "秒!")
#     WorkList = []
#     print ("成功导入数据" + str(y) + "条")
#     f.close()

#  base model
class BaseModel(models.Model):
    class Meta:
        abstract = True

    # 返回self._meta.fields中没有的，但是又是需要的字段名的列表
    # 形如['name','type']
    def getMtMField(self):
        pass

    # 返回需要在json中忽略的字段名的列表
    # 形如['password']
    def getIgnoreList(self):
        pass

    def isAttrInstance(self, attr, clazz):
        return isinstance(getattr(self, attr), clazz)

    def getDict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            # 特殊处理datetime的数据
            elif isinstance(getattr(self, attr), BaseModel):
                d[attr] = getattr(self, attr).getDict()
            # 递归生成BaseModel类的dict
            elif self.isAttrInstance(attr, int) or self.isAttrInstance(attr, float) \
                    or self.isAttrInstance(attr, str):
                d[attr] = getattr(self, attr)
            # else:
            #     d[attr] = getattr(self, attr)

        mAttr = self.getMtMField()
        if mAttr is not None:
            for m in mAttr:
                if hasattr(self, m):
                    attlist = getattr(self, m).all()
                    l = []
                    for attr in attlist:
                        if isinstance(attr, BaseModel):
                            l.append(attr.getDict())
                        else:
                            dic = attr.__dict__
                            if '_state' in dic:
                                dic.pop('_state')
                            l.append(dic)
                    d[m] = l
        # 由于ManyToMany类不能存在于_meat.fields，因而子类需要在getMtMFiled中返回这些字段
        if 'basemodel_ptr' in d:
            d.pop('basemodel_ptr')

        ignoreList = self.getIgnoreList()
        if ignoreList is not None:
            for m in ignoreList:
                if d.get(m) is not None:
                    d.pop(m)
        # 移除不需要的字段
        return d

    def toJSON(self):
        import json
        return json.dumps(self.getDict(), ensure_ascii=False).encode('utf-8').decode()

#  工具包
class utils():

    def getRandomStr(self):
        # 获取uuid的随机数
        uuid_val = uuid.uuid4()
        # 获取uuid的随机数字符串
        uuid_str = str(uuid_val).encode('utf-8')
        # 获取md5实例
        md5 = hashlib.md5()
        # 拿取uuid的md5摘要
        md5.update(uuid_str)
        # 返回固定长度的字符串
        return md5.hexdigest()

    def getMaxId(self, sql):
        list = sql.objects.all()
        if len(list) > 0:
            maxId = sql.objects.latest('id').id
        else:
            maxId = 0
        maxId += 1
        return maxId

    def headimgHandle(self, icon, sql, id):
        try:
            file_name = '%s.jpg' % str(int(time.time()))
            # 拼接一个自己的文件路径
            image_path = os.path.join('media/icons/', file_name)
            # 打开拼接的文件路径
            with open(image_path, 'wb')as fp:
                # 遍历图片的块数据（切块的传图片）
                for i in icon.chunks():
                    # 将图片数据写入自己的那个文件
                    fp.write(i)
            if id:
                imgOldPath = str(sql.objects.get(id=id).head_img)[1:]
                try :  # 假如c存在原图片，移除
                    f = open(imgOldPath)
                    f.close()
                    os.remove(imgOldPath)
                except Exception as e:
                    logger.info (str(e))
            return "/%s" % image_path
        except Exception as e:
            logger.error("图片处理失败：%s" % str(e))
            return ''

    def sendEmialText(self):
        email_title = '邮件标题'
        email_body = '邮件内容'
        email_to = 'zhaijl@grzq.com'
        cclist = ['18730585395@163.com']    # 抄送人
        msg = "测试邮件发送！"
        #  简单内容
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email_to], html_message=msg)
        if send_status:
            ret = {
                'success': True,
                'retCode': 200,
                'retMsg': "邮件添发送成功！"
            }
            return HttpResponse(json.dumps(ret), content_type='application/json')

    def sendEmialHtml(self):
        # 发件人和收件人
        sender = '2495061000@qq.com'
        receiver = 'zhaijl@grzq.com'

        # 所使用的用来发送邮件的SMTP服务器
        smtpserver = 'smtp.qq.com'

        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = '2495061000@qq.com'
        password = 'medxhyzcxodcdjhc'

        # 邮件主题
        mail_title = '主题：python邮件发送测试'

        # 读取html文件内容
        f = open('views/index.html', 'rb')  # HTML文件默认和当前文件在同一路径下，若不在同一路径下，需要指定要发送的HTML文件的路径
        mail_body = f.read()
        f.close()

        mail_body = """
            <h2>测试邮件内容html格式：</h2>
             <a href="www.baidu.com">链接导航</a>
             <p>测试段落，文本</p>
        """

        # 邮件内容, 格式, 编码
        message = MIMEText(mail_body, 'html', 'utf-8')
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = Header(mail_title, 'utf-8')

        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.qq.com')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, message.as_string())
            print("发送邮件成功！！！")
            smtp.quit()
            return True
        except smtplib.SMTPException:
            logger.error("发送邮件失败！！！")
            return False

    def sendEmialFile(self):
        # 发件人和收件人
        sender = '2495061000@qq.com'
        receiver = 'zhaijl@grzq.com'

        # 所使用的用来发送邮件的SMTP服务器
        smtpserver = 'smtp.qq.com'

        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        username = '2495061000@qq.com'
        password = 'medxhyzcxodcdjhc'

        # 邮件主题
        mail_title = '主题：python邮件发送测试'

        # 创建一个带附件的实例
        message = MIMEMultipart()
        # 构造附件1
        att1 = MIMEText(open('media/files/20190117/订饭.txt', 'rb').read(), 'html', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="OIDFrom.doc"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        message.attach(att1)
        # 构造附件2
        att2 = MIMEText(open('media/files/20190117/1111.txt', 'rb').read(), 'html', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="OIDFrom.txt"'
        message.attach(att2)

        # 邮件内容, 格式, 编码
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = Header(mail_title, 'utf-8')

        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.qq.com')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, message.as_string())
            print("发送邮件成功！！！")
            smtp.quit()
            return True
        except smtplib.SMTPException:
            logger.error("发送邮件失败！！！")
            return False

