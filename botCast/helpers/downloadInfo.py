# -*- coding:utf-8 -*-

from core.helpers.time import getTimeStamp
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.utils import debugObj

from ..helpers.prepareLinkInfo import prepareLinkInfo

_logger = getDebugLogger()


def downloadInfo(
    url: str,
    chatId: str | int | None,
    username: str,
):
    """
    This is usually the first action: to retrieve the video info from youtube.
    """
    if not isYoutubeLink(url):
        raise Exception('The url should be a valid youtube link. But we got: %s' % url)

    # Start...
    obj = {
        'url': url,
        'timeStr': getTimeStamp(),
        'chatId': chatId,
        'username': username,
    }
    debugData = debugObj(obj)
    logContent = '\n'.join(
        [
            titleStyle('downloadInfo'),
            debugData,
        ]
    )
    _logger.info(logContent)
    return prepareLinkInfo(url, username)
