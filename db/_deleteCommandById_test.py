# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_deleteCommandById_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_deleteCommandById_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _deleteCommandById_test`

import os
from typing import Optional, Final
from prisma import Prisma

from unittest import TestCase, main, mock

from db.init import closeDb, openDb

from ._testDbConfig import testEnv
from .types import TPrismaCommand
from ._deleteCommandById import deleteCommandById


@mock.patch.dict(os.environ, testEnv)
class Test_deleteCommandById_test(TestCase):

    db: Prisma

    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        cls.db = openDb()
        print('setUpClass', cls.db)

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_XXX_deleteCommandById_should_add_new_record_with_id(self):
        db: Final[Prisma] = Prisma()
        command: Optional[TPrismaCommand] = None
        try:
            # Create test record...
            if not db.is_connected():
                db.connect()
            command = db.command.create(
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
            removedCommand = db.command.find_unique(
                where={
                    'id': command.id,
                },
            )
            self.assertIsNone(removedCommand)
            db.disconnect()
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
