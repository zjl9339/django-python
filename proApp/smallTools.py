# -*-  coding:utf-8 -*-
import time

def alarm(hour, minute):
    while True:
        t = time.localtime()
        h, m, s = t[3:6]
        print ("%02d:%02d:%02d" % (h,m,s))
        if hour==h and minute ==m:
            print ("\n時間到了")
            break
        time.sleep(1)

h = int(input("請輸入小時"))
m = int(input("請輸入分鈡"))
alarm(h,m)