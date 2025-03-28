# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_prisma_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_prisma_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _prisma_test`

import os
import sys
import pathlib

from typing import Optional
from unittest import TestCase, main, mock

# from prisma import Prisma
# from prisma.models import Command

# Inject project path to allow server-side tests
sys.path.insert(1, pathlib.Path(os.getcwd()).as_posix())

# from db._testDbConfig import testEnv


# @mock.patch.dict(os.environ, testEnv)
class Test_prisma(TestCase):

    # db: Prisma

    @classmethod
    def setUpClass(cls):
        # cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        pass

    def setUp(self):
        # self.db = Prisma()
        # self.db.connect()
        pass

    def tearDown(self):
        # self.db.disconnect()
        pass

    def test_bare(self):
        self.assertTrue(True)

    # def test_prisma_should_connect(self):
    #     self.assertIsInstance(self.db, Prisma)
    #
    # def test_prisma_should_create_command(self):
    #     command: Optional[Command] = None
    #     try:
    #         command = self.db.command.create(
    #             data={
    #                 'updateId': 1,
    #                 'messageId': 1,
    #                 'userId': 1,
    #                 'userStr': 'Test user',
    #             },
    #         )
    #         # Should have numeric id property
    #         self.assertIsInstance(command.id, int)
    #     finally:
    #         # Clean up...
    #         if command:
    #             self.db.command.delete(
    #                 where={
    #                     'id': command.id,
    #                 },
    #             )


if __name__ == '__main__':
    main()
