# -*- coding:utf-8 -*-

import re


def prepareYoutubeDate(date: str | None):
    if not date:
        return ''
    ymd = re.compile(r'^(\d\d\d\d)(\d\d)(\d\d)')
    if ymd.match(date):
        return re.sub(ymd, r'\1.\2.\3', date)
    return date
