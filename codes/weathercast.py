#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime
import time

import schedule
import itchat

import citycode


# http://www.jianshu.com/p/ab8d9e576ac4

def get_forecast(url):
    info = {}
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    req = requests.get(url, headers=header)
    a = req.raise_for_status()
    # print a
    data_json = req.text
    # print (data_json)
    retdata = json.loads(data_json)
    # print (retdata)
    if retdata['status'] == 1000:
        info['retcode'] = 1
        info['data'] = retdata
    else:
        info['retcode'] = 0
        info['data'] = None
        info['errmsg'] = 'get forecast data err'
    return info


def forecast_info(forecast):
    data_info = ''''''
    for info in forecast:
        date = str2unicode(info['date'])
        we_type = str2unicode(info['type'])
        high_tem = str2unicode(info['high']).replace('高温', '最高气温：')
        low_tem = str2unicode(info['low']).replace('低温', '最低气温：')
        wind_dir = str2unicode(info['fengxiang'])
        wind_force_temp = str2unicode(info['fengli'])
        # print wind_force_temp
        wind_f = re.search('(\d+级)', wind_force_temp)
        wind_force = wind_f.group(1)
        data_info += '''
        日期：{date}
        天气状况：{we_type}
        {high_tem}, {low_tem}
        风向：{wind_dir}
        风力：{wind_force}
        '''.format(date=date, we_type=we_type, high_tem=high_tem, low_tem=low_tem, wind_dir=wind_dir,
                   wind_force=wind_force)
    return data_info
    # return mystr


def str2unicode(somestr):
    unic = somestr.encode('utf-8')
    return unic


def now_time():
    now = datetime.datetime.now()
    now_day = now.strftime('%Y年%m月%d日')
    return now_day


def format_msg(cityname, tips, forecast):
    msg = '''今天是{date},imoyao为你预报{city}天气：
{forecast}
温馨提示：{tips}

    '''.format(date=now_time(), city=cityname, forecast=forecast_info(forecast), tips=tips)
    return msg


def city_url(cityname):
    result = {}
    baseurl = 'http://wthrcdn.etouch.cn/weather_mini?citykey='
    ret = citycode.get_code(cityname)
    if ret and ret['data']:
        citykey = ret['data']
        url = baseurl + citykey
        result['data'] = url
        result['code'] = 1
        result['msg'] = ''
    else:
        res = ret['msg']
        result['data'] = None
        result['code'] = 0
        result['msg'] = res
    return result


def weather_msg():
    cityname = input('please enter the cityname:')
    url_ret = city_url(cityname)
    if url_ret and url_ret['data']:
        url = url_ret['data']
        info = get_forecast(url)
        data = info['data']
        if data:
            # print data
            # cityname = str2unicode(data['data']['city'])
            tips = str2unicode(data['data']['ganmao']) or None
            forecast = data['data']['forecast']
            res = format_msg(cityname, tips, forecast)
            return res
        else:
            errmsg = info['data']
            return errmsg
    else:
        msg = url_ret['msg']
        return msg


def time_task(jobname):
    # schedule.every(daelytime).seconds.do(printhello)
    schedule.every().day.at("06:30").do(jobname)
    while True:
        schedule.run_pending()
        time.sleep(1)


def wx_sender(gname, sendmsg):  # TODO
    # AttributeError: 'module' object has no attribute 'startfile'

    itchat.auto_login(hotReload=True)
    group = gname.decode('utf-8')
    group_name = itchat.search_chatrooms(name=group)[0]['UserName']
    # print ("group name is ",group_name)
    itchat.send_msg(msg=sendmsg.decode('utf-8'), toUserName=group_name)
    # itchat.run()


if __name__ == '__main__':
    # res = weather_msg()
    # print (res)
    wx_sender('尧', '今天发工资了')
    # wx_sender('yao','hello,world.')


newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True, statusStorageDir='newInstance.pkl')


@newInstance.msg_register(TEXT)
def reply(msg):
    return msg['Text']


newInstance.run()
