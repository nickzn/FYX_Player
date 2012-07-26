#!/usr/bin/env python -tt


import urllib2
from datetime import date
import re


def res_exist(dat):
    m = add_zero(dat.month)
    d = add_zero(dat.day)
    patt = "-%s-%s-%s-" % (dat.year, m, d)
    f = urllib2.urlopen('http://english.cri.cn/4926/more/10679/more10679.htm')
    for line in f.readlines():
        if re.search(r'htm\'>EZ Morning', line) and re.search(patt, line):
            return True
    return False


def mms_url(dat):
    m = add_zero(dat.month)
    d = add_zero(dat.day)
    d_str = "%s/%s%s" % (dat.year, m, d)

    sects = ['a', 'b', 'c']
    pre = 'mms://media.chinabroadcast.cn/eng/music/morning/'
    urls = []

    for s in sects:
        urls.append("%s%s%s.wma" % (pre, d_str, s))

    return urls


def mms_sect(url):
    m = re.search(r'\d+([a-zA-Z]+)\.wma', url)
    if m:
        return m.group(1)


def add_zero(num):
    if num < 10:
        num = '0' + str(num)
    return num


def main():
    d = date(2012, 7, 20)
    mms_urls = mms_url(d)
    print mms_urls
    print res_exist(d)
    print mms_sect(mms_urls[0])


if __name__ == '__main__':
    main()
