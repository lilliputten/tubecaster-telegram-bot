# -*- coding:utf-8 -*-


import re

# from ..constants import youtubeLinkPrefixRegex

youtubeLinkPrefixRegex = re.compile(r'^https://(\w*\.)?(youtube\.com|youtu\.be)/')


def isYoutubeLink(url: str):
    if not url:
        return False
    return youtubeLinkPrefixRegex.match(url)
