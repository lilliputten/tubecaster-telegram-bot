# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_checkCommandExistsForMessageId_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_checkCommandExistsForMessageId_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _checkCommandExistsForMessageId_test`

import os
import sys
import traceback
from typing import Optional, Final
from prisma import Prisma
import time

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._testDbConfig import testEnv
from .types import TPrismaCommand
from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId

MAXINT = 2**31 - 1


@mock.patch.dict(os.environ, testEnv)
class Test_checkCommandExistsForMessageId_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))

    def test_checkCommandExistsForMessageId_should_add_new_record_with_id(self):
        db: Final[Prisma] = Prisma()
        command: Optional[TPrismaCommand] = None
        try:
            # Create a test record...
            if not db.is_connected():
                db.connect()
            # Create a "unique" message id
            messageId = int(time.time() * 10000000) % MAXINT
            command = db.command.create(
                data={
                    'updateId': 1,
                    'messageId': messageId,
                    'userId': 1,
                    'userStr': 'Test user',
                },
            )
            # Try to remove...
            isExists = checkCommandExistsForMessageId(messageId)
            # Try to find supposed to be absent...
            testCommand = db.command.find_unique(
                where={
                    'id': command.id,
                },
            )
            self.assertTrue(isExists)
            if not testCommand:
                raise Exception('Created command should exist')
            # A value of `repeated` property should be incremented
            self.assertEqual(testCommand.repeated, 2)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            # Clean up...
            if db:
                if command:
                    if not db.is_connected():
                        db.connect()
                    db.command.delete(
                        where={
                            'id': command.id,
                        },
                    )
                if db.is_connected():
                    db.disconnect()


if __name__ == '__main__':
    main()
