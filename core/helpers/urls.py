# -*- coding:utf-8 -*-


from ..constants import youtubeLinkPrefixRegex


def isYoutubeLink(url: str):
    if not url:
        return False
    return youtubeLinkPrefixRegex.match(url)
