# -*-  coding:utf-8 -*-
import logging
logger = logging.getLogger('django')
from proApp.common import utils

#  定时任务
class tasks():
    def test(self):
        print ("sched.add_job 固定时间启动")

    def testFuncton(self):
        print("Hello Scheduler")




