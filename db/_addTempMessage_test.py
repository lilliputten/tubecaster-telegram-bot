# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
import traceback
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._addTempMessage import addTempMessage
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from ._types import TTempMessage
from .models import Command, TempMessage


@mock.patch.dict(os.environ, testEnv)
class Test_addTempMessage_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def setUp(self):
        session = initDb()
        self.command = Command(
            updateId=randrange(1, 9999),
            messageId=randrange(1, 9999),
            userId=randrange(1, 9999),
            userStr='Test',
        )
        session.add(self.command)
        session.commit()

    def tearDown(self):
        if self.command:
            session = initDb()
            command = session.get(Command, self.command.id)
            if command:
                session.delete(command)
                session.commit()
            self.command = None

    def test_addTempMessage_should_add_new_item_with_id(self):
        tempMessage: Optional[TTempMessage] = None
        try:
            if self.command:
                tempMessage = addTempMessage(commandId=self.command.id, messageId=self.command.messageId)
            self.assertIsInstance(tempMessage, TTempMessage)
            if tempMessage:
                self.assertIsInstance(tempMessage.id, int)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if tempMessage:
                session = initDb()
                db_temp = session.get(TempMessage, tempMessage.id)
                if db_temp:
                    session.delete(db_temp)
                    session.commit()

    def test_addTempMessage_should_be_removed_if_command_deleted(self):
        tempMessage: Optional[TTempMessage] = None
        try:
            session = initDb()
            if self.command:
                tempMessage = addTempMessage(commandId=self.command.id, messageId=self.command.messageId)
                command = session.get(Command, self.command.id)
                if command:
                    session.delete(command)
                    session.commit()
                self.command = None
            if not tempMessage:
                raise Exception('No temp message has been created')
            testTempMessage = session.get(TempMessage, tempMessage.id)
            self.assertIsNone(testTempMessage)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if tempMessage:
                session = initDb()
                db_temp = session.get(TempMessage, tempMessage.id)
                if db_temp:
                    session.delete(db_temp)
                    session.commit()


if __name__ == '__main__':
    main()
