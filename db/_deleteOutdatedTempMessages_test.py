# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_deleteOutdatedTempMessages_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_deleteOutdatedTempMessages_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _deleteOutdatedTempMessages_test`

import datetime
import os
from random import randrange
import time
import traceback
from typing import Optional
from prisma.models import Command
from prisma.models import TempMessage

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._init import closeDb, initDb

from ._testDbConfig import testEnv
from ._types import TPrismaCommand, TTempMessage
from ._deleteOutdatedTempMessages import deleteOutdatedTempMessages


@mock.patch.dict(os.environ, testEnv)
class Test_deleteOutdatedTempMessages_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteOutdatedTempMessages_should_delete_old_tempMessages(self):
        command: Optional[TPrismaCommand] = None
        tempMessage: Optional[TTempMessage] = None
        try:
            commandClient = Command.prisma()
            tempMessageClient = TempMessage.prisma()
            now = datetime.datetime.now(datetime.timezone.utc)
            # Create a record 2 days back to the past and set outdated range 1 day closer to the current time
            createdAt = now - datetime.timedelta(days=2)
            outdatedDate = now - datetime.timedelta(days=1)
            updateId = randrange(1, 9999)
            messageId = randrange(1, 9999)
            userId = randrange(1, 9999)
            userStr = 'Test user'
            # createdAt = createdAt
            command = commandClient.create(
                data={
                    'updateId': updateId,
                    'messageId': messageId,
                    'userId': userId,
                    'userStr': userStr,
                    'createdAt': createdAt,
                },
            )
            tempMessage = tempMessageClient.create(
                data={
                    'commandId': command.id,
                    # 'updateId': updateId,
                    'messageId': messageId,
                    # 'userId': userId,
                    # 'userStr': userStr,
                    'createdAt': createdAt,
                },
            )
            # Try to remove...
            deleteOutdatedTempMessages(outdatedDate=outdatedDate)
            # Try to find supposed to be absent...
            removedTempMessage = tempMessageClient.find_unique(
                where={
                    'id': tempMessage.id,
                },
            )
            self.assertIsNone(removedTempMessage)
            tempMessage = None
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
            raise Exception(errMsg)
        finally:
            # Clean up...
            if tempMessage:
                tempMessageClient = TempMessage.prisma()
                tempMessageClient.delete(
                    where={
                        'id': tempMessage.id,
                    },
                )
            if command:
                commandClient = Command.prisma()
                commandClient.delete(
                    where={
                        'id': command.id,
                    },
                )


if __name__ == '__main__':
    main()
