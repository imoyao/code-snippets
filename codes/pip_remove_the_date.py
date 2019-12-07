#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/7 13:33
"""
Usage:
修改 specific_time（like:2019-12-07）,以找到该日期之后安装的 pip 包
"""
import os
import time
import datetime
from pip._internal.utils.misc import get_installed_distributions


def get_all_packages():
    """
    see also: https://stackoverflow.com/questions/10256093/how-to-convert-ctime-to-datetime-in-python
    获取到所有安装的 packages
    :return:
    """
    install_packages = get_installed_distributions()
    return install_packages


def get_after_date_packages(date=None):
    """
    获取指定日期之后安装的 package
    :param date:str, like:2019-12-07
    :return:
    """
    if not date:
        date = datetime.datetime.today().strftime('%Y-%m-%d')

    install_packages = get_all_packages()
    for package in install_packages:
        package_ctime = os.path.getctime(package.location)  # package 创建时间
        time_array = time.localtime(package_ctime)
        strftime_package = time.strftime("%Y-%m-%d", time_array)

        if strftime_package >= date:  # 转换为 %Y-%m-%d 之后比较大小
            # 打印安装时间和 package 名称
            print(time.strftime('%Y-%m-%d-%H:%M:%S', time_array), package)


if __name__ == '__main__':
    specific_time = '2019-11-06'
    get_after_date_packages(specific_time)
