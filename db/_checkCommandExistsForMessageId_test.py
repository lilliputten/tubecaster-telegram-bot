# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
import traceback
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from ._types import TPrismaCommand
from .models import Command


@mock.patch.dict(os.environ, testEnv)
class Test_checkCommandExistsForMessageId_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_checkCommandExistsForMessageId_should_add_new_record_with_id(self):
        command: Optional[TPrismaCommand] = None
        try:
            session = initDb()
            messageId = randrange(1, 9999)
            command = Command(
                messageId=messageId,
                updateId=randrange(1, 9999),
                userId=randrange(1, 9999),
                userStr='Test',
            )
            session.add(command)
            session.commit()
            isExists = checkCommandExistsForMessageId(messageId)
            testCommand = session.get(Command, command.id)
            self.assertTrue(isExists)
            if not testCommand:
                raise Exception('Created command should exist')
            self.assertEqual(testCommand.repeated, 2)
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
