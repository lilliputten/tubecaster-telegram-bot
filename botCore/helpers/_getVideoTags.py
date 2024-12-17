import re

from botCore.types import TVideoInfo


def getVideoTags(videoInfo: TVideoInfo):
    channel = videoInfo.get('channel')
    channelTag = re.sub(r'\W+', '_', channel.strip()) if channel else ''
    return ' '.join(
        list(
            filter(
                None,
                [
                    '#TubeCaster',
                    '#Audio',
                    '#' + channelTag if channelTag else '',
                ],
            )
        )
    )
