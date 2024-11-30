# -*- coding:utf-8 -*-

from datetime import datetime


# TODO: Move these to constants/config?
idTimeFormat = '%Y-%m-%d-%H-%M-%S'
shortTimeFormat = '%Y-%m-%d %H:%M'
defaultTimeFormat = '%Y-%m-%d %H:%M:%S'
preciseTimeFormat = defaultTimeFormat + ',%f'


# TODO: blue error: Cannot parse: type Precise = bool | str
#  type Precise = str


def getTimeFormat(precise: bool | str | None = None):
    if precise == True or precise == 'precise':
        return preciseTimeFormat
    if precise == 'short':
        return shortTimeFormat
    if precise == 'id':
        return idTimeFormat
    return defaultTimeFormat


def formatTime(precise: bool | str | None = None):
    format = getTimeFormat(precise)
    stamp = datetime.today().strftime(format)
    if precise == True or precise == 'precise':
        stamp = stamp[:-3]
    return stamp


def getTimeStamp(precise: bool | str | None = None):
    format = getTimeFormat(precise)
    stamp = datetime.today().strftime(format)
    if precise == True or precise == 'precise':
        stamp = stamp[:-3]
    return stamp
