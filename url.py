#!/usr/bin/env python -tt


import urllib2
from datetime import date
import re


def res_exist(dat):
    m = add_zero(dat.month)
    d = add_zero(dat.day)
    patt = "<a\s*href='(.*htm)'>EZ Morning.*-%s-%s-%s-.*<\/a>" % (dat.year, m, d)
    base_url = 'http://english.cri.cn'
    f = urllib2.urlopen('%s/4926/more/10679/more10679.htm' % base_url)
    for line in f.readlines():
        m = re.search(patt, line)
        if m:
            return '%s%s' % (base_url, m.group(1))
    return False


def mms_url(dat):
    urls = []
    url = res_exist(dat)
    f = urllib2.urlopen(url)
    patt = "'file'\s*:\s*'(.*)'"
    for line in f.readlines():
        m = re.search(patt, line)
        if m:
            urls.append(m.group(1))
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
    d = date(2013, 6, 28)
    mms_urls = mms_url(d)
    print mms_urls
    print mms_sect(mms_urls[0])


if __name__ == '__main__':
    main()
