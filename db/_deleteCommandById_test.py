# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
from typing import Optional
from unittest import TestCase, main, mock

from ._deleteCommandById import deleteCommandById
from ._init import closeDb, initDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from ._types import TPrismaCommand
from .models import Command


@mock.patch.dict(os.environ, testEnv)
class Test_deleteCommandById_test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_deleteCommandById_should_add_new_record_with_id(self):
        command: Optional[TPrismaCommand] = None
        try:
            session = initDb()
            command = Command(
                updateId=1,
                messageId=1,
                userId=1,
                userStr='Test user',
            )
            session.add(command)
            session.commit()
            deleteCommandById(command.id)
            removedCommand = session.get(Command, command.id)
            self.assertIsNone(removedCommand)
            command = None
        finally:
            if command:
                session = initDb()
                db_command = session.get(Command, command.id)
                if db_command:
                    session.delete(db_command)
                    session.commit()


if __name__ == '__main__':
    main()
