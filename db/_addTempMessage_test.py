# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_addTempMessage_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_addTempMessage_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _addTempMessage_test`

import os
from random import randrange
import traceback
from typing import Optional, Final
from prisma import Prisma

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._testDbConfig import testEnv
from .types import TPrismaCommand, TTempMessage
from ._addTempMessage import addTempMessage


@mock.patch.dict(os.environ, testEnv)
class Test_addTempMessage_test(TestCase):

    db: Final[Prisma] = Prisma()
    command: Optional[TPrismaCommand]

    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))

    def setUp(self):
        # self.db = Prisma()
        self.db.connect()
        # Create base command
        self.command = self.db.command.create(
            data={
                'updateId': randrange(1, 9999),
                'messageId': randrange(1, 9999),
                'userId': randrange(1, 9999),
                'userStr': 'Test',
            },
        )

    def tearDown(self):
        if self.command:
            self.db.command.delete(
                where={
                    'id': self.command.id,
                },
            )
            self.command = None
        self.db.disconnect()

    def test_addTempMessage_should_add_new_item_with_id(self):
        tempMessage: Optional[TTempMessage] = None
        try:
            # Create temp message
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
                self.db.tempmessage.delete(
                    where={
                        'id': tempMessage.id,
                    },
                )

    def test_addTempMessage_should_be_removed_if_command_deleted(self):
        tempMessage: Optional[TTempMessage] = None
        try:
            # Create temp message
            if self.command:
                tempMessage = addTempMessage(commandId=self.command.id, messageId=self.command.messageId)
                # Remove basic command
                self.db.command.delete(
                    where={
                        'id': self.command.id,
                    },
                )
                self.command = None
            if not tempMessage:
                raise Exception('No temp message has been created')
            # Try to find temp message again
            testTempMessage = self.db.tempmessage.find_unique(
                where={
                    'id': tempMessage.id,
                },
            )
            self.assertIsNone(testTempMessage)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if tempMessage:
                self.db.tempmessage.delete(
                    where={
                        'id': tempMessage.id,
                    },
                )


if __name__ == '__main__':
    main()
