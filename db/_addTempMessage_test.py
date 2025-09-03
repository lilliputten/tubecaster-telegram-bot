# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_addTempMessage_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_addTempMessage_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _addTempMessage_test`

import os
import traceback
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from prisma.models import Command, TempMessage

from core.helpers.errors import errorToString

from ._addTempMessage import addTempMessage
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._types import TTempMessage


@mock.patch.dict(os.environ, testEnv)
class Test_addTempMessage_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def setUp(self):
        # Create base command
        commandClient = Command.prisma()
        self.command = commandClient.create(
            data={
                'updateId': randrange(1, 9999),
                'messageId': randrange(1, 9999),
                'userId': randrange(1, 9999),
                'userStr': 'Test',
            },
        )

    def tearDown(self):
        if self.command:
            commandClient = Command.prisma()
            commandClient.delete(
                where={
                    'id': self.command.id,
                },
            )
            self.command = None

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
                tempMessageClient = TempMessage.prisma()
                tempMessageClient.delete(
                    where={
                        'id': tempMessage.id,
                    },
                )

    def test_addTempMessage_should_be_removed_if_command_deleted(self):
        tempMessage: Optional[TTempMessage] = None
        try:
            commandClient = Command.prisma()
            tempMessageClient = TempMessage.prisma()
            # Create temp message
            if self.command:
                tempMessage = addTempMessage(commandId=self.command.id, messageId=self.command.messageId)
                # Remove basic command
                commandClient.delete(
                    where={
                        'id': self.command.id,
                    },
                )
                self.command = None
            if not tempMessage:
                raise Exception('No temp message has been created')
            # Try to find temp message again
            testTempMessage = tempMessageClient.find_unique(
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
                tempMessageClient = TempMessage.prisma()
                tempMessageClient.delete(
                    where={
                        'id': tempMessage.id,
                    },
                )


if __name__ == '__main__':
    main()
