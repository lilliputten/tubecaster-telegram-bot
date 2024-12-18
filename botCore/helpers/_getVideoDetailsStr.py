# -*- coding:utf-8 -*-

from datetime import timedelta

from ..types import TVideoInfo
from ._prepareYoutubeDate import prepareYoutubeDate
from ._getFormattedVideoFileSize import getFormattedVideoFileSize


def getVideoDetailsStr(videoInfo: TVideoInfo):
    videoSizeFmt = getFormattedVideoFileSize(videoInfo)
    return ', '.join(
        filter(
            None,
            [
                str(timedelta(seconds=int(videoInfo['duration']))) if videoInfo.get('duration') else None,
                videoSizeFmt,
                videoInfo.get('resolution'),  # '640x360'
                str(videoInfo.get('fps')) + ' fps' if videoInfo.get('fps') else None,
                prepareYoutubeDate(videoInfo.get('upload_date')),  # '20160511'
            ],
        )
    )
