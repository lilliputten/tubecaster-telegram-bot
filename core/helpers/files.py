import os
import re

from ..constants import youtubeLinkPrefixRegex


def getIdFromName(name: str):
    filename = name  # .lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    filename = re.sub(r'\s+', '-', filename)
    return filename


def getFileIdFromUrl(url: str, username: str):
    filename = url
    filename = re.sub(youtubeLinkPrefixRegex, '', filename)
    filename = getIdFromName(filename)
    filename = re.sub(r'^watch-v-', '', filename)
    if username:
        filename = getIdFromName(username) + '-' + filename
    return filename


def sizeofFmt(num, suffix='B'):
    #  if num == 0:
    #      return '0'
    if not num:
        return ''
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def getFormattedFileSize(fileName: str | None):
    audioSize = os.path.getsize(fileName) if fileName else None
    return sizeofFmt(audioSize)
