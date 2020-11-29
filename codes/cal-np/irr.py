#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/11/29 20:39
import numpy as np

START_INVEST = 140000
INVEST_MONTH = 12
EVERY_MONTH_INVEST = 10000


def cal_irr_invest_in_month(every_month_invest: int, invest_month: int, start_invest: int) -> float:
    cal_list = [every_month_invest] * invest_month
    cal_list.append(-start_invest)
    profile = np.irr(cal_list)
    return (pow(profile + 1, 12) - 1) * 100


print(cal_irr_invest_in_month(EVERY_MONTH_INVEST, INVEST_MONTH, START_INVEST))
