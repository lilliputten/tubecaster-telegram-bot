# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_checkCommandExistsForMessageId_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_checkCommandExistsForMessageId_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _checkCommandExistsForMessageId_test`

import os
import traceback
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from prisma.models import Command

from core.helpers.errors import errorToString

from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._types import TPrismaCommand


@mock.patch.dict(os.environ, testEnv)
class Test_checkCommandExistsForMessageId_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_checkCommandExistsForMessageId_should_add_new_record_with_id(self):
        # db: Final[Prisma] = Prisma()
        command: Optional[TPrismaCommand] = None
        try:
            commandClient = Command.prisma()
            # Create a "unique" message id
            messageId = randrange(1, 9999)
            command = commandClient.create(
                data={
                    'messageId': messageId,
                    'updateId': randrange(1, 9999),
                    'userId': randrange(1, 9999),
                    'userStr': 'Test',
                },
            )
            # Try to remove...
            isExists = checkCommandExistsForMessageId(messageId)
            # Try to find supposed to be absent...
            testCommand = commandClient.find_unique(
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
            if command:
                commandClient = Command.prisma()
                commandClient.delete(
                    where={
                        'id': command.id,
                    },
                )


if __name__ == '__main__':
    main()
