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

        page = get_page_number()
        print '有' + str(page) + '页'
        update_ids = get_list_info(page)

        # main_detail()
        start_no = 0
        end_no = len(update_ids)
        thread_num = 5
        while start_no < (end_no - thread_num + 1):
            threads = []

            for inner_index in range(0, thread_num):
                threads.append(threading.Thread(target=get_info, args=(update_ids[start_no + inner_index],)))
            for t in threads:
                t.setDaemon(True)
                t.start()
            t.join()
            start_no += thread_num


        print '休息一天'
        time.sleep(86400)

