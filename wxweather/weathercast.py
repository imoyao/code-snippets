#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import re
import json
import datetime
import time
import traceback

import schedule
import itchat


def city_info():
    try:
        with open('./cityinfo.json', 'r') as f:
            code_str = json.load(f)
        proviences = code_str['CityCode']
        county_dict = {}
        county_list = []
        for pro in proviences:
            cityList = pro['cityList']
            for city in cityList:
                countyList = city['countyList']
                for county in countyList:
                    name = county['name']
                    code = county['code']
                    county_dict[name] = code
        return county_dict
    except Exception as e:
        traceback.print_exc()


def get_code(cityname):
    try:
        result = {}
        city = cityname.decode('utf-8')
        county_dict = city_info()
        if city in county_dict:
            code = county_dict[city]
            result['retcode'] = 1
            result['data'] = code
            result['msg'] = ''
        else:
            result['retcode'] = 0
            result['data'] = None
            result['msg'] = 'please check your enter.'
        return result
    except Exception as e:
        traceback.print_exc()


def city_url(cityname):
    try:
        result = {}
        baseurl = 'http://wthrcdn.etouch.cn/weather_mini?citykey='
        ret = get_code(cityname)
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
    except Exception as e:
        traceback.print_exc()


def get_forecast(url):
    try:
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
    except Exception as e:
        traceback.print_exc()


def forecast_info(cityname, tips, forecast):
    try:
        data_info = ''''''
        for info in forecast:
            date = encode_str(info['date'])
            we_type = encode_str(info['type'])
            high_tem = encode_str(info['high']).replace('高温', '最高气温：')
            low_tem = encode_str(info['low']).replace('低温', '最低气温：')
            wind_dir = encode_str(info['fengxiang'])
            wind_force_temp = encode_str(info['fengli'])
            # print wind_force_temp
            wind_f = re.search('(\d+级)', wind_force_temp)
            wind_force = wind_f.group(1)
            data_info += '''
    日期：{date}
    天气状况：{we_type}
    {high_tem}
    {low_tem}
    风向：{wind_dir}
    风力：{wind_force}
                '''.format(date=date, we_type=we_type, high_tem=high_tem, low_tem=low_tem, wind_dir=wind_dir,
                           wind_force=wind_force)

        msg = '''今天是{today},imoyao为你预报{city}天气：
        {forecast}
温馨提示：{tips}'''.format(today=now_time(), city=cityname, forecast=data_info, tips=tips)
        return msg
    except Exception as e:
        traceback.print_exc()


def weather_msg(cityname):
    try:
        url_ret = city_url(cityname)
        if url_ret and url_ret['data']:
            url = url_ret['data']
            info = get_forecast(url)
            data = info['data']
            if data:
                tips = encode_str(data['data']['ganmao']) or None
                forecast = data['data']['forecast']
                res = forecast_info(cityname, tips, forecast)
                return res
            else:
                errmsg = info['data']
                return errmsg
        else:
            msg = url_ret['msg']
            return msg
    except Exception as e:
        traceback.print_exc()


def wx_sender(gname, sendmsg):  # TODO
    try:
        newInstance = itchat.new_instance()
        newInstance.auto_login(
            hotReload=True, statusStorageDir='newInstance.pkl')
        # itchat.auto_login(hotReload=True)
        group = decode_str(gname)
        group_name = newInstance.search_chatrooms(name=group)[0]['UserName']
        msg_str = decode_str(sendmsg)
        if group_name:
            newInstance.send_msg(msg=msg_str, toUserName=group_name)
    except Exception as e:
        traceback.print_exc()


def time_task(jobname, *args):
    try:
        job_name = jobname.__name__
        # TODO:if err,try again.one more time,send msg to admin.
        if 'weather_msg' in job_name:
            schedule.every().day.at("06:00").do(jobname, *args)
        elif 'wx_sender' in job_name:
            schedule.every().day.at("06:30").do(jobname, *args)
            # schedule.every(30).seconds.do(jobname, *args)
        elif job_name:
            schedule.every(5).seconds.do(jobname, *args)
        else:
            pass
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        traceback.print_exc()


def sumnum(num1, num2):  # for test
    sum_num = num1+num2
    return sum_num


def decode_str(somestr):
    de_str = somestr.decode('utf-8')
    return de_str


def encode_str(somestr):
    en_str = somestr.encode('utf-8')
    return en_str


def now_time():
    now = datetime.datetime.now()
    now_day = now.strftime('%Y年%m月%d日')
    return now_day


def main():
    cityname = raw_input('please enter the cityname:')
    gname = 'imoyao'  # The group to send msg
    msg = weather_msg(cityname)  # How to change msg……
    # print(msg)
    time_task(wx_sender, gname, msg)

if __name__ == '__main__':
    main()
