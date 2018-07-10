#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from send_email_to_me import holidays_2018
from send_email_to_me import holidays_2019


def get_days_left(date_from, str_date_to):
    days = (datetime.datetime.strptime(str_date_to, '%Y/%m/%d') - date_from).days
    return days


def is_holiday(target):
    holidays = holidays_2018.HOLIDAYS
    holidays.extend(holidays_2019.HOLIDAYS)
    for h in holidays:
        if h.day == target.day and h.month == target.month and h.year == target.year:
            return True
    return False


def get_days_off(date_from, str_date_to):
    date_to = datetime.datetime.strptime(str_date_to, '%Y/%m/%d')
    days_left = get_days_left(date_from, str_date_to)
    result = 0
    for i in range(1, (days_left + 1)):
        target = date_from + datetime.timedelta(days=i)
        if is_holiday(target) or target.weekday() in (5, 6):
            result = result + 1
    return result
