# -*- coding: utf-8 -*-
# @Time         : 2018/2/5 10:18
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : run.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : yuecai

from yucai_spider_update import *
from yucai_spider_detail import *

if __name__ == '__main__':
    while True:

        main_update()

        main_detail()

        print '休息6小时'
        time.sleep(21600)

