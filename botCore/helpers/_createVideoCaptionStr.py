# -*- coding:utf-8 -*-

from datetime import timedelta

from core.ffmpeg import probe
from core.helpers.files import getFormattedFileSize
from core.helpers.strings import truncStr

from ..types import TVideoInfo
from ..constants import emojies

from ._getVideoTags import getVideoTags
from ._getVideoDetailsStr import getVideoDetailsStr

#  from ._getFormattedVideoFileSize import getFormattedVideoFileSize
#  from ._prepareYoutubeDate import prepareYoutubeDate

_maxCaptionLength = 1024

def createVideoCaptionStr(
    videoInfo: TVideoInfo,
    audioFileName: str,
    pieceNo: int | None = None,
    piecesCount: int | None = None,
):
    pieceInfo = f'{pieceNo + 1}/{piecesCount}' if pieceNo != None and piecesCount else None
    # Get audio duration (via ffmpeg probe)...
    probeData = probe(audioFileName)
    format = probeData.get('format', {})
    durationPrecise = float(format.get('duration', '0'))   # 1.811156
    duration = round(durationPrecise)
    durationFmt = str(timedelta(seconds=duration))
    # Audio file size...
    audioSizeFmt = getFormattedFileSize(audioFileName)
    # Video file size...
    #  videoSizeFmt = getFormattedVideoFileSize(videoInfo)
    videoDetails = getVideoDetailsStr(videoInfo)
    captionStr = ' — '.join(
        filter(
            None,
            [
                videoInfo.get('channel'),
                videoInfo.get('title'),
            ],
        )
    )
    if pieceInfo:
        captionStr += ', part ' + pieceInfo
    captionStr = emojies.success + ' ' + captionStr
    detailsContent = ' '.join(
        filter(
            None,
            [
                'The audio',
                #  pieceInfo,
                f'({durationFmt}, {audioSizeFmt})' if audioSizeFmt else '',
                'has been extracted from the video',
                f'({videoDetails})' if videoDetails else '',
                #  videoInfo.get('webpage_url'),
            ],
        )
    )
    #  # NOTE: Temporarily disabled as too noisy
    #  infoContent = '\n'.join(
    #      filter(
    #          None,
    #          [
    #              # fmt: off
    #              #  'Channel: %s' % videoInfo.get('channel'),  # '进出口服务（AHUANG）'
    #              #  'Title: %s' % videoInfo.get('title'),
    #              #  'Video link: %s' % videoInfo.get('webpage_url'),
    #              'Duration: %s' % timedelta(seconds=int(videoInfo['duration'])) if videoInfo.get('duration') else None,
    #              'Upload date: %s' % prepareYoutubeDate(videoInfo.get('upload_date')),  # '20160511'
    #              'Audio size: %s' % audioSizeFmt,
    #              'Video size: %s' % videoSizeFmt,
    #              'Resolution: %s' % videoInfo.get('resolution'),
    #              'FPS: %s' % videoInfo.get('fps'),
    #              'Language: %s' % videoInfo.get('language'),
    #              #  'Tags: %s' % ', '.join(videoInfo['tags']) if videoInfo.get('tags') else None,  # [...]
    #              #  'Categories: %s' % ', '.join(videoInfo['categories']) if videoInfo.get('categories') else None,  # [...]
    #              #  'Comments count: %s' % videoInfo.get('comment_count'),
    #              #  'Views count: %s' % videoInfo.get('view_count'),
    #              #  'Audio channels: %s' % videoInfo.get('audio_channels'),  # 2
    #              # fmt: on
    #          ],
    #      )
    #  )
    tagsContent = getVideoTags(videoInfo)
    captionContent = '\n\n'.join(
        filter(
            None,
            [
                captionStr,
                detailsContent,
                videoInfo.get('webpage_url'),
                #  infoContent,
                tagsContent,
            ],
        )
    )
    if len(captionContent) >= _maxCaptionLength:
        captionContent = truncStr(captionContent, _maxCaptionLength)
    return captionContent
