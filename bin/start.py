# -*- coding: utf-8 -*-
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = "%s/jd" % BASE_DIR
command = "cd %s; scrapy crawl jd; cd -" % path

while True:
    os.system(command)
    time.sleep(60 * 60)  # 每小时执行一次
