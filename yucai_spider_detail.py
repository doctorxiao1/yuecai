# -*- coding: utf-8 -*-
# @Time         : 2018/1/29 09:45
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : yucai_spider_detail.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : yuecai

import time
import MySQLdb
import requests
import random
import datetime
import re
import threading
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')


def re2_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def re_findall(pattern, html):
    if re.findall(pattern, html):
        return re.findall(pattern, html)
    else:
        return 'N'


def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    # detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')
    return detag


def get_chinese(str):
    b = re.compile(u"[\u4e00-\u9fa5]*")
    c = "".join(b.findall(str.decode('utf8')))
    return c


def get_number(str):
    b = re.compile(u".|\d*")
    c = "".join(b.findall(str.decode('utf8')))
    return c


def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


def get_parse(url):
    while True:
        try:
            index = random.randint(1, len(proxies) - 1)
            proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
            print 'Now Proxy is : ' + str(proxy) + ' @ ' + str(datetime.datetime.now())
            response = requests.get(url, timeout=10, proxies=proxy)
            if response.status_code == 200:
                return response
                # return response
                break
            else:
                return None
                break
        except Exception, e:

            print e
            if str(e).find('HTTPSConnectionPool') >= 0:
                time.sleep(3)
                continue
            elif str(e).find('HTTPConnectionPool') >= 0:
                time.sleep(3)
                continue
            else:
                return None
                break


def get_need_ids():
    conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                           charset="utf8")
    cursor = conn.cursor()

    cursor.execute('select id from purchase_yuecai_list')
    all = []
    all_ids = cursor.fetchall()
    for x in range(0, len(all_ids)):
        all.append(all_ids[x][0])

    cursor.execute('select id from purchase_yuecai_detail')
    old = []
    old_ids = cursor.fetchall()
    for y in range(0, len(old)):
        old.append(old_ids[y][0])
    cursor.close()
    conn.close()
    print '获取过的内容 处理完毕 old_urls ready '

    need_ids = []
    for need_id in all:
        if need_id not in old:
            need_ids.append(need_id)

    return need_ids


def get_info(id):
    try:
        conn = MySQLdb.connect(host="221.226.72.226", port=13306, user="root", passwd="somao1129", db="tanke",
                               charset="utf8")
        cursor = conn.cursor()
        if len(id) <= 10:
            url = 'http://www.yuecai.com/purchase/sj-' + id + '.htm'
            print url
            content_1 = get_parse(url)
            content = str(content_1.text)

            # print content
            if content.__contains__('招标人'):
                print '检测到 招标 信息'

                title = re.findall('<title>(.*?)_.*?</title>', content)[0]
                print title

                corp_name = re.findall('<dd class="bg"><a target="_blank" href=".*?" title="(.*?)">', content)[0]
                print corp_name

                project_num = re.findall('<em id="progect_num">(.*?)</em></span>', content)[0]
                print project_num

                beginDate = re.findall('<em id="beginDate">(.*?)</em></p>', content)[0]
                print beginDate

                endDate = re.findall('<em id="endDate">(.*?)</em></p>', content)[0]
                print endDate

                region = re.findall('<p title="(.*?)">', content)[0]
                print region

                business_type = re.findall('<p title="(.*?)">', content)[1]
                print business_type

                industry = re.findall('<p title="(.*?)">', content)[2]
                print industry

                if content.find('进行中') >= 0:
                    state = '进行中'
                else:
                    state = '已结束'

                print state

                project_name = re_findall('<br/>项目名称：(.*?)<br/>', content)[0]
                print project_name

                tenderer = re_findall('<br/>招标人：(.*?)<br/>', content)[0]
                print tenderer

                tender_method = re_findall('<br/>招标方式：(.*?)<br/>', content)[0]
                print tender_method

                buy_tender_file = re_findall('<br/>招标文件领购：(.*?)<br/>', content)[0]
                print buy_tender_file

                tender_bond = re_findall('<br/>投标保证金：(.*?)<br/>', content)[0]
                print tender_bond

                buy_tender_file_start_time = re_findall('招标文件领购开始时间：(.*?)<br/>', content)[0]
                print buy_tender_file_start_time

                buy_tender_file_end_time = re_findall('<br/>招标文件领购截止时间：(.*?)<br/>', content)[0]
                print buy_tender_file_end_time

                tender_deadline = re_findall('<br/>投标截止时间：(.*?)<br/>', content)[0]
                print tender_deadline

                tender_file_buy_address = re_findall('<br/>招标文件领购地址：(.*?)<br/>', content)[0]
                print tender_file_buy_address

                tender_file_accept_address = re_findall('<br/>投标文件接收地址：(.*?)<br/>', content)[0]
                print tender_file_accept_address

                other_info = re_findall('<br/>投标文件接收地址.*?<br/>(.*?)<br/></p>', content)[0]
                print detag(other_info)

                cursor.execute(
                    'insert into tender_yuecai_detail values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (
                        id,
                        url,
                        title,
                        corp_name,
                        project_num,
                        beginDate,
                        endDate,
                        region,
                        business_type,
                        industry,
                        project_name,
                        tenderer,
                        tender_method,
                        buy_tender_file,
                        tender_bond,
                        buy_tender_file_start_time,
                        buy_tender_file_end_time,
                        tender_deadline,
                        tender_file_buy_address,
                        tender_file_accept_address,
                        detag(other_info),

                        str(datetime.datetime.now()),
                        str(datetime.datetime.now())[:10]
                    ))
                conn.commit()
                print str(id) + ' 插入招标信息成功 ' + ' _@_ ' + str(datetime.datetime.now())



            else:
                print '检测到 采购 信息'

                title = re.findall('<title>(.*?)_.*?</title>', content)[0]
                print title

                corp_name = re.findall('<dd class="bg"><a target="_blank" href=".*?" title="(.*?)">', content)[0]
                print corp_name

                project_num = re.findall('<em id="progect_num">(.*?)</em></span>', content)[0]
                print project_num

                beginDate = re.findall('<em id="beginDate">(.*?)</em></p>', content)[0]
                print beginDate

                endDate = re.findall('<em id="endDate">(.*?)</em></p>', content)[0]
                print endDate

                region = re.findall('<p title="(.*?)">', content)[0]
                print region

                business_type = re.findall('<p title="(.*?)">', content)[1]
                print business_type

                industry = re.findall('<p title="(.*?)">', content)[2]
                print industry

                if content.find('进行中') >= 0:
                    state = '进行中'
                else:
                    state = '已结束'

                print state

                product = re.findall('<span class="titlecu" title="(.*?)">', content)
                info = ''
                for x in range(len(product)):
                    product_name = product[x]
                    # print product_name

                    product_num = re.findall('<span title="(.*?)">.*?</span>', content)[x * 3]
                    # print product_num

                    product_specification = re.findall('<span title="(.*?)">.*?</span>', content)[x * 3 + 1]
                    # print product_specification

                    product_unit = re.findall('<span title="(.*?)">.*?</span>', content)[x * 3 + 2]
                    # print product_unit

                    info += '|第' + str(
                        x + 1) + '项-->名称:' + product_name + '|品目:' + product_num + '|规格:' + product_specification + '|单位:' + product_unit + '||'

                print info

                project_describe = \
                    re2_findall('<h1 class="title_m">项目信息</h1>(.*?)</p>', content)[0]
                print detag(project_describe)

                requirement_for_supplier = \
                    re2_findall('<h1 class="title_m">对供应商的要求</h1>(.*?)</p>', content)[0]
                print detag(requirement_for_supplier)

                cursor.execute(
                    'insert into purchase_yuecai_detail values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (
                        id,
                        url,
                        title,
                        corp_name,
                        project_num,
                        beginDate,
                        endDate,
                        region,
                        business_type,
                        industry,
                        info,
                        detag(project_describe),
                        detag(requirement_for_supplier),

                        str(datetime.datetime.now()),
                        str(datetime.datetime.now())[:10]
                    ))
                conn.commit()
                print str(id) + ' 插入采购信息成功 ' + ' _@_ ' + str(datetime.datetime.now())

        else:
            print '检测到 竞价 信息'
            url_2 = 'http://www.yuecai.com/purchase/auctionDetail-' + id + '.htm'
            print url_2
            content_2 = get_parse(url_2)
            content2 = str(content_2.text)
            print content2

            title = re.findall('<title>(.*?)_.*?</title>', content2)[0]
            print title

            corp_name = re.findall('<dd class="bg"><a target="_blank" href=".*?" title="(.*?)">', content2)[0]
            print corp_name

            project_num = re.findall('<em id="progect_num">(.*?)</em></span>', content2)[0]
            print project_num

            beginDate = re.findall('<p class="deadline">发布时间:<span>(.*?)</span></p>', content2)[0]
            print beginDate

            endDate = re.findall('<p class="deadline">竞价时间:<span>(.*?)</span></p>', content2)[0]
            print endDate

            region = re.findall('<p title="(.*?)">', content2)[0]
            print region

            business_type = re.findall('<p title="(.*?)">', content2)[1]
            print business_type

            industry = re.findall('<p title="(.*?)">', content2, re.S)[2]
            print industry

            product_len = len(re.findall('<td title="(.*?)">', content2))

            product_info = ''
            for num in range(product_len):
                product_name = re.findall('<td >(.*?)</td>', content2)[6 * num + 1]

                product_bidcode_t = re.findall('<td >(.*?)</td>', content2)[6 * num + 2]

                product_specification = re.findall('<td title="(.*?)">', content2)[num]

                product_purchase_num = re.findall('<td >(.*?)</td>', content2)[6 * num + 3]

                product_unit = re.findall('<td >(.*?)</td>', content2)[6 * num + 4]

                product_planned_price = re.findall('<td >(.*?)</td>', content2)[6 * num + 5]

                product_info += '|第' + str(
                    num + 1) + '项-->采购品名称:' + product_name + '|采购品编码:' + product_bidcode_t + '|规格:' + product_specification + '|采购量:' + product_purchase_num + '|单位:' + product_unit + '|计划价(元):' + product_planned_price + '||'

            print product_info

            # 竞价项目基本信息
            bid_result = re.findall('<td class="td-left">竞价结果：</td>(.*?)</span></td>', content2, re.S)[0]

            print get_chinese(bid_result)

            bid_type = re.findall('<td class="td-left">项目类型：</td>(.*?)</span></td>', content2, re.S)[0]
            print get_chinese(bid_type)

            unite = \
                re.findall('<td class="td-right"><span>(.*?)</span></td>', content2)
            # print unite
            # for x in unite:
            #     print x
            # print '-------------'

            bid_currency = unite[0]
            print bid_currency

            bid_brief = unite[1]
            print bid_brief

            contact = unite[2]
            print contact

            phone = unite[3]
            print phone

            fax = unite[4]
            print fax

            email = unite[5]
            print email

            # 竞价条款
            delivery_mode = unite[6]
            print delivery_mode

            pay_mode = unite[7]
            print pay_mode

            delivery_time = re.findall('<td class="td-right"><span.*?>(.*?)</span></td>', content2)[8]
            print delivery_time

            pay_place = unite[8]
            print pay_place

            tax = unite[9]
            print tax

            documents = unite[10]
            print '竞价文件: ' + documents

            buy_documents_time = unite[10]
            print '购买竞价文件时间：' + buy_documents_time

            buy_documents_place = unite[11]
            print '购买竞价文件地点：' + buy_documents_place

            documents_price = re.findall('<td class="td-right"><span>(.*?)</td>', content2)[13]

            print '竞价文件售价：' + documents_price

            bid_place = unite[13]
            print '竞价地点：' + bid_place

            bond = unite[14]
            print '保证金：	' + bond

            # 竞价规则

            bid_start_time = unite[15]
            print bid_start_time
            unite2 = re.findall('<td class="td-right"><span>(.*?)</span></td>', content2, re.S)

            bid_range = get_chinese(unite2[19])
            print 'bid_range : ' + detag(bid_range)

            bid_method = get_chinese(unite2[20])
            print 'bid_method : ' + detag(bid_method)

            minimum_price_reduction = unite2[21].replace('\t', '').strip()
            # print 'minimum_price_reduction :' + get_number(minimum_price_reduction)

            print minimum_price_reduction

            bid_end_time = unite[16]
            print bid_end_time

            postponement_rules = unite2[23]
            print 'postponement_rules :' + detag(postponement_rules.strip())

            minimum_price_difference_limit = unite2[24]
            print 'minimum_price_difference_limit :' + detag(minimum_price_difference_limit.strip())

            show_bid_or_not = unite[17]
            print show_bid_or_not

            cursor.execute(
                'insert into bid_yuecai_detail values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                (
                    id,
                    url_2,
                    title,
                    corp_name,
                    project_num,
                    beginDate,
                    endDate,
                    region,
                    business_type,
                    industry,
                    product_info,
                    get_chinese(bid_result),
                    get_chinese(bid_type),
                    bid_currency,
                    bid_brief,
                    contact,
                    phone,
                    fax,
                    email,
                    delivery_mode,
                    pay_mode,
                    delivery_time,
                    pay_place,
                    tax,
                    documents,
                    buy_documents_time,
                    buy_documents_place,
                    documents_price,
                    bid_place,
                    bond,
                    bid_start_time,
                    detag(bid_range),
                    detag(bid_method),
                    minimum_price_reduction,
                    bid_end_time,
                    detag(postponement_rules.strip()),
                    detag(minimum_price_difference_limit.strip()),
                    show_bid_or_not,

                    str(datetime.datetime.now()),
                    str(datetime.datetime.now())[:10]
                ))
            conn.commit()
            print str(id) + ' 插入 竞价 信息成功 ' + ' _@_ ' + str(datetime.datetime.now())
    except:
        print traceback.format_exc()


def main():
    need_ids = get_need_ids()

    start_no = 0
    end_no = len(need_ids)
    thread_num = 5
    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=get_info, args=(need_ids[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num


if __name__ == '__main__':
    proxies = get_proxy()
    main()

