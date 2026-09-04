# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import datetime
import os
import traceback
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._deleteOutdatedTempMessages import deleteOutdatedTempMessages
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from ._types import TPrismaCommand, TTempMessage
from .models import Command, TempMessage


@mock.patch.dict(os.environ, testEnv)
class Test_deleteOutdatedTempMessages_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteOutdatedTempMessages_should_delete_old_tempMessages(self):
        command: Optional[TPrismaCommand] = None
        tempMessage: Optional[TTempMessage] = None
        try:
            session = initDb()
            now = datetime.datetime.now(datetime.timezone.utc)
            createdAt = now - datetime.timedelta(days=2)
            outdatedDate = now - datetime.timedelta(days=1)
            command = Command(
                updateId=randrange(1, 9999),
                messageId=randrange(1, 9999),
                userId=randrange(1, 9999),
                userStr='Test user',
                createdAt=createdAt,
            )
            session.add(command)
            session.commit()
            tempMessage = TempMessage(
                commandId=command.id,
                messageId=command.messageId,
                createdAt=createdAt,
            )
            session.add(tempMessage)
            session.commit()
            deleteOutdatedTempMessages(outdatedDate=outdatedDate)
            removedTempMessage = session.get(TempMessage, tempMessage.id)
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
            if tempMessage:
                session = initDb()
                db_temp = session.get(TempMessage, tempMessage.id)
                if db_temp:
                    session.delete(db_temp)
                    session.commit()
            if command:
                session = initDb()
                db_command = session.get(Command, command.id)
                if db_command:
                    session.delete(db_command)
                    session.commit()


if __name__ == '__main__':
    main()
