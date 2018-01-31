# -*- coding: utf-8 -*-
# @Time         : 2018/1/25 10:08
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : yucai_spider_all.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : yuecai

import json
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')
from requests.exceptions import RequestException
import urllib3

urllib3.disable_warnings()

import re
import time
import requests
import threading
import random
import datetime
import MySQLdb

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'iris.yuecai.com',
    'Content-Type': 'application/json',
    'Origin': 'http://www.yuecai.com',
    'Content-Length': '71',
    'Referer': 'http://www.yuecai.com/purchase/?SiteID=21&start=20&page=1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_timestamp(normal_time):
    timeArray = time.strptime(str(normal_time), "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return timestamp


def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


def get_page_number():
    payload = {"word": None, "zone": None, "page": 1, "size": 20, "sort": None, "teseData": 2}
    url = 'http://iris.yuecai.com/iris/v1/purchase/search'
    try:

        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
        if response.status_code == 200:
            content = json.loads(response.text)
            return content['resultData']['totalPages']
        else:
            print '获取页数出错'
            return None
    except Exception, e:
        print str(e)


def get_list_info(page):
    conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                           charset="utf8")
    cursor = conn.cursor()

    url = 'http://iris.yuecai.com/iris/v1/purchase/search'
    while True:
        try:
            for x in range(1, int(page) + 1):
                payload2 = {"word": None, "zone": None, "page": x, "size": 20, "sort": None, "teseData": 2}

                response = requests.post(url, data=json.dumps(payload2), headers=headers, timeout=30)

                info = json.loads(response.text)

                total_pages = len(info['resultData']['data'])

                for num in range(1, total_pages + 1):

                    id_tag = info['resultData']['data'][num]['id']
                    create_time = info['resultData']['data'][num]['pubDate']
                    type = info['resultData']['data'][num]['projectType']

                    if id_tag not in old_ids:
                        if type == '采购':

                            cursor.execute('replace into purchase_yuecai_list values ("%s","%s","%s","%s")' %
                                           (
                                               id_tag,
                                               create_time,

                                               str(datetime.datetime.now()),
                                               str(datetime.datetime.now())[:10]
                                           ))
                            conn.commit()
                            print str(id_tag) + '  插入成功 _@_ ' + str(datetime.datetime.now())
                            break
                        elif type == '竞价':
                            bidcode_t = info['resultData']['data'][num]['bidcode_t']
                            companyId = info['resultData']['data'][num]['companyId']
                            id_tag = info['resultData']['data'][num]['id']

                            url_part = bidcode_t + '-' + companyId + '-' + id_tag
                            cursor.execute('replace into purchase_yuecai_list values ("%s","%s","%s","%s")' %
                                           (
                                               url_part,
                                               create_time,

                                               str(datetime.datetime.now()),
                                               str(datetime.datetime.now())[:10]
                                           ))
                            conn.commit()
                            print str(id_tag) + '  插入成功 _@_ ' + str(datetime.datetime.now())
                            break
                        elif type == '招标':
                            cursor.execute('replace into purchase_yuecai_list values ("%s","%s","%s","%s")' %
                                           (
                                               id_tag,
                                               create_time,

                                               str(datetime.datetime.now()),
                                               str(datetime.datetime.now())[:10]
                                           ))
                            conn.commit()
                            print str(id_tag) + '  插入成功 _@_ ' + str(datetime.datetime.now())
                            break


                    else:
                        print '检测到已爬信息  ' + str(id_tag) + ' _@_ ' + str(datetime.datetime.now())
                        # else:
                        #     id_tag = info['resultData']['data'][num]['id']
                        #     create_time = info['resultData']['data'][num]['pubDate']
                        #     cursor.execute('insert into purchase_yuecai_list values ("%s","%s","%s","%s")' %
                        #                    (
                        #                        id_tag,
                        #                        create_time,
                        #                        str(datetime.datetime.now()),
                        #                        str(datetime.datetime.now())[:10]
                        #                    ))
                        #     conn.commit()
                        #     print str(id_tag) + '  插入成功'
                        break
        except Exception, e:
            if str(e).find('2006') >= 0:
                print '休息两秒 重连数据库(2006)'
                time.sleep(2)

                conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                                       charset="utf8")
                cursor = conn.cursor()

                continue

            elif str(e).find('2013') >= 0:
                print '休息两秒 重连数据库(2013)'
                conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                                       charset="utf8")
                cursor = conn.cursor()
                continue
            else:

                print traceback.format_exc()
                break


def main():
    page = get_page_number()
    print '有' + str(page) + '页'
    get_list_info(page)




if __name__ == '__main__':
    conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                           charset="utf8")
    cursor = conn.cursor()

    # cursor.execute('select max(createtime) from purchase_yuecai_list')
    # max_create_time = cursor.fetchall()[0][0]

    old_ids = []
    cursor.execute('select id from purchase_yuecai_list')
    old = cursor.fetchall()
    for y in range(0, len(old)):
        old_ids.append(old[y][0])
    cursor.close()
    conn.close()
    print '获取过的内容 处理完毕 old_urls ready '

    main()
