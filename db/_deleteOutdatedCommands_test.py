# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import datetime
import os
import traceback
from typing import Optional
from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._deleteOutdatedCommands import deleteOutdatedCommands
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from ._types import TPrismaCommand
from .models import Command


@mock.patch.dict(os.environ, testEnv)
class Test_deleteOutdatedCommands_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteOutdatedCommands_should_delete_old_commands(self):
        command: Optional[TPrismaCommand] = None
        try:
            session = initDb()
            now = datetime.datetime.now(datetime.timezone.utc)
            createdAt = now - datetime.timedelta(days=2)
            outdatedDate = now - datetime.timedelta(days=1)
            command = Command(
                updateId=1,
                messageId=1,
                userId=1,
                userStr='Test user',
                createdAt=createdAt,
            )
            session.add(command)
            session.commit()
            deleteOutdatedCommands(outdatedDate=outdatedDate)
            removedCommand = session.get(Command, command.id)
            self.assertIsNone(removedCommand)
            command = None
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if command:
                session = initDb()
                db_command = session.get(Command, command.id)
                if db_command:
                    session.delete(db_command)
                    session.commit()


if __name__ == '__main__':
    main()
