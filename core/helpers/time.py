# -*- coding:utf-8 -*-

from datetime import datetime, timedelta, timezone
from threading import Timer

from core.appConfig import TZ_HOURS_OFFSET

# TODO: Move these to constants/config?
idTimeFormat = '%Y-%m-%d-%H-%M-%S'
yearMonthFormat = '%Y-%m'
onlyDateTimeFormat = '%Y-%m-%d'
shortTimeFormat = '%Y-%m-%d %H:%M'
shortTzTimeFormat = '%Y-%m-%d %H:%M %z'
withSecondsTimeFormat = '%Y-%m-%d %H:%M:%S'
withSecondsTzTimeFormat = '%Y-%m-%d %H:%M:%S %z'
shortTimeFormatWithSeconds = '%Y-%m-%d %H:%M:%S'
preciseTimeFormat = shortTimeFormatWithSeconds + ',%f'

tzObject = timezone(timedelta(hours=int(TZ_HOURS_OFFSET) or 0))  # if TZ_HOURS != None else None

TPrecise = bool | str

TDateLike = datetime | int | float


def ensureCorrectDateTime(date: TDateLike | None = None):
    dateVal: datetime
    if type(date) is int or type(date) is float:   # isinstance(date, int):
        dateFloat = float(date)
        dateVal = datetime.fromtimestamp(dateFloat)
    elif date and type(date) is datetime:
        dateVal = date
    else:
        dateVal = datetime.now(tzObject)
    if dateVal.tzinfo is None:
        dateVal = dateVal.replace(tzinfo=tzObject)
    return dateVal


def getCurrentDateTime():
    return datetime.now(tzObject)


def getTimeFormat(precise: TPrecise | None = None):
    if precise == True or precise == 'precise':
        return preciseTimeFormat
    if precise == 'yearMonth':
        return yearMonthFormat
    if precise == 'shortTz':
        return shortTzTimeFormat
    if precise == 'onlyDate':
        return onlyDateTimeFormat
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
    dateVal = ensureCorrectDateTime(date)
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
