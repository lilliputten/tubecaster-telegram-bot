# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_addCommand_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_addCommand_test.py`
#  - `poetry run python -m unittest discover -v -f -t . -s . -p "*_test.py" -k _addCommand_test`

import os
from typing import Optional

from prisma.models import Command

from unittest import TestCase, main, mock

from ._init import closeDb, initDb

from ._testDbConfig import testEnv
from ._types import TNewCommandData, TPrismaCommand
from ._addCommand import addCommand


@mock.patch.dict(os.environ, testEnv)
class Test_addCommand_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_addCommand_should_add_new_record_with_id(self):
        command: Optional[TPrismaCommand] = None
        try:
            data: TNewCommandData = {
                'updateId': 1,
                'messageId': 1,
                'userId': 1,
                'userStr': 'Test user',
            }
            command = addCommand(data)
            self.assertIsInstance(command, TPrismaCommand)
            self.assertIsInstance(command.id, int)
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
