# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_addCommand_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_addCommand_test.py`
#  - `poetry run python -m unittest discover -v -f -t . -s . -p "*_test.py" -k _addCommand_test`

import traceback

from unittest import TestCase, main

from ._probeDuration import probeDuration

audioFile = 'tests/test-audios/sample-with-wrong-metadata-duration/file.mp3'


class Test_probeDuration_test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_probeDuration_should_return_correct_value(self):
        try:
            duration = probeDuration(audioFile)
            self.assertEqual(duration, 167.183673)
        except Exception as err:
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            print('ERROR:', repr(err))
            print('Traceback:', sTraceback)


if __name__ == '__main__':
    main()
