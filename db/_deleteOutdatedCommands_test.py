# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_deleteOutdatedCommands_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_deleteOutdatedCommands_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _deleteOutdatedCommands_test`

import datetime
import os
import time
import traceback
from typing import Optional
from prisma.models import Command

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._init import closeDb, initDb

from ._testDbConfig import testEnv
from ._types import TPrismaCommand
from ._deleteOutdatedCommands import deleteOutdatedCommands


@mock.patch.dict(os.environ, testEnv)
class Test_deleteOutdatedCommands_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteOutdatedCommands_should_delete_old_commands(self):
        command: Optional[TPrismaCommand] = None
        try:
            commandClient = Command.prisma()
            now = datetime.datetime.now(datetime.timezone.utc)
            # Create a record 2 days back to the past and set outdated range 1 day closer to the current time
            createdAt = now - datetime.timedelta(days=2)
            outdatedDate = now - datetime.timedelta(days=1)
            command = commandClient.create(
                data={
                    'updateId': 1,
                    'messageId': 1,
                    'userId': 1,
                    'userStr': 'Test user',
                    'createdAt': createdAt,
                },
            )
            # Try to remove...
            deleteOutdatedCommands(outdatedDate=outdatedDate)
            # Try to find supposed to be absent...
            removedCommand = commandClient.find_unique(
                where={
                    'id': command.id,
                },
            )
            self.assertIsNone(removedCommand)
            command = None
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
            #  raise Exception(errMsg)
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
