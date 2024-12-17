import re

from ..types import TVideoInfo


def createTagItem(s: str | None):
    return ('#' + re.sub(r'\W+', '_', s.strip())) if s else ''


def getVideoTags(videoInfo: TVideoInfo):
    channel = videoInfo.get('channel')
    # TODO: Remove non-unique tags
    tags: list[str] | None = videoInfo.get('tags')
    tagsStr = ' '.join(map(createTagItem, tags)) if tags else None
    return ' '.join(
        filter(
            None,
            [
                '#TubeCaster',
                '#Audio',
                createTagItem(channel),
                tagsStr,
            ],
        )
    )
