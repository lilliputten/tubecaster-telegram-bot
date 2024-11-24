# -*- coding:utf-8 -*-

from datetime import datetime

# TODO: Move these to constants/config?
defaultTimeFormat = '%Y-%m-%d %H:%M:%S'
preciseTimeFormat = defaultTimeFormat + ',%f'


def getTimeStamp(precise: bool | None):
    format = preciseTimeFormat if precise else defaultTimeFormat
    stamp = datetime.today().strftime(format)
    if precise:
        stamp = stamp[:-3]
    return stamp
