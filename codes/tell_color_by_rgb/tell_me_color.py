#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/4/15 22:23
import re
from functools import wraps, partial
from collections.abc import Iterable

COLOR_BASE_MAP = {
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'lime': (0, 255, 0),
    'cyan': (0, 255, 255),
    'blue': (0, 0, 255),
    'magenta': (255, 0, 255),
}
# 因为黑白我们的算法基本可以识别所以此处不列出
REG_COLOR_SERES = r'\w*([灰|红|黄|绿|青|蓝|紫])\w*'
# 'black', 'gray', 'white', 'red', 'yellow', 'green', 'cyan', 'blue', 'purple'
COLOR_SERIES_MAP = {
    'black': '黑',
    'gray': '灰',
    'white': '白',
    'red': '红',
    'yellow': '黄',
    'green': '绿',
    'cyan': '青',
    'blue': '蓝',
    'purple': '紫'
}

COLOR_SERIES_MAP_REVERSE = {'黑': 'black', '灰': 'gray', '白': 'white', '红': 'red', '黄': 'yellow', '绿': 'green',
                            '青': 'cyan', '蓝': 'blue', '紫': 'purple'}


def hue_calculate(round1, round2, delta, add_num):
    return (((round1 - round2) / delta) * 60 + add_num) % 360


def rgb_to_hsv(rgb_seq):
    assert isinstance(rgb_seq, Iterable)
    assert len(rgb_seq) == 3
    r, g, b = rgb_seq
    r_round = float(r) / 255
    g_round = float(g) / 255
    b_round = float(b) / 255
    max_c = max(r_round, g_round, b_round)
    min_c = min(r_round, g_round, b_round)
    delta = max_c - min_c

    h = None
    if delta == 0:
        h = 0
    elif max_c == r_round:
        h = hue_calculate(g_round, b_round, delta, 360)
    elif max_c == g_round:
        h = hue_calculate(b_round, r_round, delta, 120)
    elif max_c == b_round:
        h = hue_calculate(r_round, g_round, delta, 240)
    if max_c == 0:
        s = 0
    else:
        s = (delta / max_c) * 100
    v = max_c * 100
    return h, s, v


def hue_calculate_org(round1, round2, delta, add_num):
    return ((round1 - round2) / delta + add_num) * 60


def rgb_to_hsv_org(rgb_seq):
    assert isinstance(rgb_seq, Iterable)
    assert len(rgb_seq) == 3
    r, g, b = rgb_seq
    r_round = float(r) / 255
    g_round = float(g) / 255
    b_round = float(b) / 255
    max_c = max(r_round, g_round, b_round)
    min_c = min(r_round, g_round, b_round)
    delta = max_c - min_c
    h = None
    if delta == 0:
        h = 0
    elif max_c == r_round:
        h = ((g_round - b_round) / delta % 6) * 60

    elif max_c == g_round:
        h = hue_calculate_org(b_round, r_round, delta, 2)
    elif max_c == b_round:
        h = hue_calculate_org(r_round, g_round, delta, 4)
    if max_c == 0:
        s = 0
    else:
        s = delta / max_c
    return h, s, max_c


def update_by_value(v):
    """
    根据 V 值去更新色系数据
    :param v:
    :return:
    """
    if v <= 100 / 3 * 1:
        cs = 'black'
    elif v <= 100 / 3 * 2:
        cs = 'gray'
    else:
        cs = 'white'
    return cs


def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def find_color_series_by_name(name=''):
    """
    装饰器：通过颜色的中文名称利用正则匹配获取颜色名称
    参见《Python Cookbook 中文版》V3 p342 9.5：定义一个属性可由用户修改的装饰器
    我们假定命名是符合人类主观意识的，即：名称比我们的代码更可靠
    因为按照hsv去匹配的时候会有误差，所以我们先通过名称去直接匹配色系，如果名称中没有关键字，我们再使用自己写的规则
    :param name:
    :return:
    """

    def deco(func):
        color_name_char = name

        @wraps(func)
        def wrapper(*args, **kwargs):
            color_series = ''
            if color_name_char:
                re_ret = re.match(REG_COLOR_SERES, color_name_char)
                if re_ret:
                    color_signal = re_ret.group(1)
                    color_series = COLOR_SERIES_MAP_REVERSE.get(color_signal)

            if color_series == '':
                color_series = func(*args, **kwargs)
            return color_series

        @attach_wrapper(wrapper)
        def set_color_name(new_name):
            nonlocal color_name_char
            color_name_char = new_name

        return wrapper

    return deco


@find_color_series_by_name(name='')
def find_color_series(rgb_seq):  # TODO:此处是否有更好实现？
    """
    将rgb转为hsv之后根据h和v寻找色系
    :param rgb_seq:
    :return:
    """
    h, s, v = rgb_to_hsv(rgb_seq)
    cs = None
    if 30 < h <= 90:
        cs = 'yellow'
    elif 90 < h <= 150:
        cs = 'green'
    elif 150 < h <= 210:
        cs = 'cyan'
    elif 210 < h <= 270:
        cs = 'blue'
    elif 270 < h <= 330:
        cs = 'purple'
    elif h > 330 or h <= 30:
        cs = 'red'

    if s < 10:  # 色相太淡时，显示什么颜色主要由亮度来决定
        cs = update_by_value(v)
    assert cs in COLOR_SERIES_MAP
    return cs


if __name__ == '__main__':

    test_color_map = {'东方红': [254, 223, 225], '红东方': [215, 196, 187], '方红东': [86, 46, 55], '黄丹': [240, 94, 28],
                      '万红丛中一点绿': [63, 43, 54]}
    for k, v in test_color_map.items():
        find_color_series.set_color_name(k)
        find_color = find_color_series(v)
        print(find_color)
