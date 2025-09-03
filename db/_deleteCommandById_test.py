# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_deleteCommandById_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_deleteCommandById_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _deleteCommandById_test`

import os
from typing import Optional
from unittest import TestCase, main, mock

from prisma.models import Command

from ._deleteCommandById import deleteCommandById
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._types import TPrismaCommand


@mock.patch.dict(os.environ, testEnv)
class Test_deleteCommandById_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteCommandById_should_add_new_record_with_id(self):
        command: Optional[TPrismaCommand] = None
        try:
            commandClient = Command.prisma()
            command = commandClient.create(
                data={
                    'updateId': 1,
                    'messageId': 1,
                    'userId': 1,
                    'userStr': 'Test user',
                },
            )
            # Try to remove...
            deleteCommandById(command.id)
            # Try to find supposed to be absent...
            removedCommand = commandClient.find_unique(
                where={
                    'id': command.id,
                },
            )
            self.assertIsNone(removedCommand)
            command = None
        # except Exception as err:
        #     errText = errorToString(err, show_stacktrace=False)
        #     sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        #     errMsg = 'Error: ' + errText
        #     print('Traceback for the following error:' + sTraceback)
        #     print('Error: ' + errMsg)
        #     #  raise Exception(errMsg)
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
