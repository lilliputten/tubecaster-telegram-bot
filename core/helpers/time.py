# -*- coding:utf-8 -*-

from datetime import datetime
from threading import Timer


# TODO: Move these to constants/config?
idTimeFormat = '%Y-%m-%d-%H-%M-%S'
shortTimeFormat = '%Y-%m-%d %H:%M'
defaultTimeFormat = '%Y-%m-%d %H:%M:%S'
preciseTimeFormat = defaultTimeFormat + ',%f'


# TODO: blue error: Cannot parse: type Precise = bool | str
TPrecise = bool | str

TDateLike = datetime | int


def getTimeFormat(precise: TPrecise | None = None):
    if precise == True or precise == 'precise':
        return preciseTimeFormat
    if precise == 'short':
        return shortTimeFormat
    if precise == 'id':
        return idTimeFormat
    return defaultTimeFormat


def formatTime(precise: TPrecise | None = None, date: TDateLike | None = None):
    format = getTimeFormat(precise)
    if not date:
        date = datetime.today()
    elif isinstance(date, int):   # type(date) == 'int':
        dateFloat = float(date)
        date = datetime.fromtimestamp(dateFloat)
    stamp = date.strftime(format)
    if precise == True or precise == 'precise':
        stamp = stamp[:-3]
    return stamp


def getTimeStamp(precise: TPrecise | None = None, date: TDateLike | None = None):
    return formatTime(precise, date)
    #  format = getTimeFormat(precise)
    #  if not date:
    #      date = datetime.today()
    #  stamp = date.strftime(format)
    #  if precise == True or precise == 'precise':
    #      stamp = stamp[:-3]
    #  return stamp


class RepeatedTimer(object):
    """
    Repeating timer helper class
    """

    def __init__(self, interval: float, function, *args, **kwargs):
        self._timer: Timer | None = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.isRunning: bool = False
        self.start()

    def _run(self):
        self.isRunning = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.isRunning:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.isRunning = True

    def stop(self):
        if self._timer:
            self._timer.cancel()
        self.isRunning = False
