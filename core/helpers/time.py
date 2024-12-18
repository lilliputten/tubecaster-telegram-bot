# -*- coding:utf-8 -*-

from datetime import datetime, timezone, timedelta
from threading import Timer

from core.appConfig import TZ_HOURS


# TODO: Move these to constants/config?
idTimeFormat = '%Y-%m-%d-%H-%M-%S'
shortTimeFormat = '%Y-%m-%d %H:%M'
shortTzTimeFormat = '%Y-%m-%d %H:%M %z'
withSecondsTimeFormat = '%Y-%m-%d %H:%M:%S'
withSecondsTzTimeFormat = '%Y-%m-%d %H:%M:%S %z'
shortTimeFormatWithSeconds = '%Y-%m-%d %H:%M:%S'
preciseTimeFormat = shortTimeFormatWithSeconds + ',%f'

tzObject = timezone(timedelta(hours=int(TZ_HOURS))) if TZ_HOURS != None else None

# TODO: blue error: Cannot parse: type Precise = bool | str
TPrecise = bool | str

TDateLike = datetime | int


def getTimeFormat(precise: TPrecise | None = None):
    if precise == True or precise == 'precise':
        return preciseTimeFormat
    if precise == 'shortTz':
        return shortTzTimeFormat
    if precise == 'short':
        return shortTimeFormat
    if precise == 'withSeconds':
        return withSecondsTimeFormat
    if precise == 'withSecondsTz':
        return withSecondsTzTimeFormat
    if precise == 'id':
        return idTimeFormat
    return withSecondsTzTimeFormat


def formatTime(precise: TPrecise | None = None, date: TDateLike | None = None):
    format = getTimeFormat(precise)
    dateVal: datetime
    if type(date) is int:   # isinstance(date, int):
        dateFloat = float(date)
        dateVal = datetime.fromtimestamp(dateFloat)
    elif type(date) is datetime and date:
        dateVal = date
    else:
        dateVal = datetime.now(tzObject)
    stamp = dateVal.strftime(format).strip()
    if precise == True or precise == 'precise':
        stamp = stamp[:-3]
    return stamp


def getTimeStamp(precise: TPrecise | None = None, date: TDateLike | None = None):
    return formatTime(precise, date)


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
