# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_getVideoTags_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_getVideoTags_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _getVideoTags_test`

from unittest import TestCase, main

from ..types import TVideoInfo
from ._getVideoTags import getVideoTags


class Test_getVideoTags(TestCase):
    def test_getVideoTags_shouldProcessChannelName(self):
        videoInfo: TVideoInfo = {
            'channel': 'Channel name',
        }
        tags = getVideoTags(videoInfo)
        self.assertIn('Channel_name', tags)

    def test_getVideoTags_shouldProcessOtherTags(self):
        videoInfo: TVideoInfo = {
            'tags': ['Tag 1', 'Tag 2'],
        }
        tags = getVideoTags(videoInfo)
        self.assertIn('#Tag_1', tags)


if __name__ == '__main__':
    main()
