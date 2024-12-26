# -*- coding:utf-8 -*-

from datetime import timedelta

from core.ffmpeg import probe, probeDuration
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
    pieceInfo = f'{pieceNo + 1}/{piecesCount}' if pieceNo != None and piecesCount and piecesCount > 1 else None
    # Get audio duration (via ffmpeg probe)...
    # probeData = probe(audioFileName)
    # format = probeData.get('format', {})
    # durationPrecise = float(format.get('duration', '0'))   # 1.811156
    # duration = round(durationPrecise)
    duration = probeDuration(audioFileName)
    durationFmt = str(timedelta(seconds=round(duration)))
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
    captionPrefix = emojies.success
    if pieceInfo and pieceNo != None and pieceNo + 1 < len(emojies.numbers):
        captionPrefix = emojies.numbers[pieceNo + 1]
    captionStr = captionPrefix + ' ' + captionStr
    # fmt: off
    detailsContent = ' '.join(filter(None, [
        emojies.card,
        'The audio',
        #  pieceInfo,
        f'({durationFmt}, {audioSizeFmt})',
        'has been extracted from the video',
        f'({videoDetails})' if videoDetails else '',
        #  videoInfo.get('webpage_url'),
    ]))
    # fmt: on
    # # NOTE: Temporarily disabled as too noisy
    # infoContent = '\n'.join(filter( None, [
    #     # fmt: off
    #     #  'Channel: %s' % videoInfo.get('channel'),  # '进出口服务（AHUANG）'
    #     #  'Title: %s' % videoInfo.get('title'),
    #     #  'Video link: %s' % videoInfo.get('webpage_url'),
    #     'Duration: %s' % timedelta(seconds=int(videoInfo['duration'])) if videoInfo.get('duration') else None,
    #     'Upload date: %s' % prepareYoutubeDate(videoInfo.get('upload_date')),  # '20160511'
    #     'Audio size: %s' % audioSizeFmt,
    #     'Video size: %s' % videoSizeFmt,
    #     'Resolution: %s' % videoInfo.get('resolution'),
    #     'FPS: %s' % videoInfo.get('fps'),
    #     'Language: %s' % videoInfo.get('language'),
    #     #  'Tags: %s' % ', '.join(videoInfo.get('tags')) if videoInfo.get('tags') else None,  # [...]
    #     #  'Categories: %s' % ', '.join(videoInfo.get('categories')) if videoInfo.get('categories') else None,  # [...]
    #     #  'Comments count: %s' % videoInfo.get('comment_count'),
    #     #  'Views count: %s' % videoInfo.get('view_count'),
    #     #  'Audio channels: %s' % videoInfo.get('audio_channels'),  # 2
    #     # fmt: on
    # ]))
    tagsContent = getVideoTags(videoInfo)
    # fmt: off
    captionContent = '\n\n'.join(filter(None, [
        captionStr,
        '%s Part %s' % (emojies.no, pieceInfo) if pieceInfo else None,
        detailsContent,
        '%s %s' % (emojies.video, videoInfo.get('webpage_url')) if videoInfo.get('webpage_url') else None,
        #  infoContent,
        '%s %s' % (emojies.tag, tagsContent) if tagsContent else None,
    ]))
    # fmt: on
    if len(captionContent) >= _maxCaptionLength:
        captionContent = truncStr(captionContent, _maxCaptionLength)
    return captionContent
