#!/usr/bin/env python -tt


import calendar
from datetime import date
import re


def main():
    dates = default_dates()
    days_str = date_str(dates)
    print days_str
    d = str_date('2012-7-21')
    print d.year, d.month, d.day


def default_dates():
    c = calendar.Calendar(0)
    today = date.today()
    y = today.year
    m = today.month
    d = today.day

    dates = []
    weeks = c.monthdatescalendar(y, m)
    weeks.reverse()
    for lsts in weeks:
        lsts.reverse()
        for da in lsts:
            if da.month <= m and is_week(da) and da.day <= d: dates.append(da)
            if len(dates) == 10:
                dates.reverse()
                return dates


def is_week(d):
    if d.weekday() >= 0 and d.weekday() <= 4:
        return True
    else:
        return False


def date_str(dats):
    strs = []
    for dat in dats:
        strs.append("%-4s-%2s-%2s" % (dat.year, dat.month, dat.day))
    return strs


def str_date(str):
    m = re.search(r'(\d+)-\s*(\d+)-\s*(\d+)', str)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


if __name__ == '__main__':
    main()
