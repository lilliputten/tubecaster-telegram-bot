# -*- coding:utf-8 -*-
# @module utils
# @since 2020.02.23, 02:18
# @changed 2024.02.29, 00:19


import re
import traceback


def empty(var):
    return not var and var is None


def notEmpty(var):
    return not empty(var)


def hasNotEmpty(obj, key):
    return obj and key in obj and notEmpty(obj[key])


def getObjKey(obj, key):
    return obj[key] if obj and key in obj else None


def msTimeFromSec(sec):
    return sec * 1000


def msTimeFromMin(min):
    return msTimeFromSec(min * 60)


def msTimeFromHours(hrs):
    return msTimeFromMin(hrs * 60)


def quoteStr(s, addQuotes=False, quoteDouble=False, quoteSingle=True):
    """
    s (str) -- Source string parameter.
    Options:
    - addQuotes (bool|str) -- Add quotes around result string (default: False, don't quote).
    - quoteSingle (bool) -- Quote single quotes ('), default is True.
    - quoteDouble (bool) -- Quote double quotes ("), default is False.
    Returns string.
    """
    if not isinstance(s, str):  # type(s) != str:
        if s is None:
            s = ''
        else:
            s = str(s)
    if quoteDouble:
        s = s.replace('"', '\\"')
    if quoteSingle:
        s = s.replace("'", "\\'")
    if addQuotes:
        if addQuotes is True:
            addQuotes = "'"
        s = addQuotes + s + addQuotes
    return s


def dictFromModule(module):
    dict = {}
    for setting in dir(module):
        # you can write your filter here
        if not setting.startswith('__'):
            dict[setting] = getattr(module, setting)
    return dict


def dictFromClass(cls):
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        #  if key not in _excluded_keys
    )


def truncateLongString(s, maxLength=0):
    if maxLength and len(s) >= maxLength:
        s = s[0 : maxLength - 3] + '...'
    return s


def prepareLongString(s, maxLength=0):
    s = re.sub(r'\s+\n', '\n', s)
    return truncateLongString(s, maxLength)


def capitalize_id(id: str):
    if id == 'uuid':
        return 'UUID'
    text = re.sub(r'_', ' ', id)
    text = text.capitalize()
    return text


__all__ = [  # Exporting objects...
    'empty',
    'notEmpty',
    'hasNotEmpty',
    'getObjKey',
    'msTimeFromSec',
    'msTimeFromMin',
    'quoteStr',
    'dictFromClass',
    'truncateLongString',
    'prepareLongString',
    'capitalize_id',
]
