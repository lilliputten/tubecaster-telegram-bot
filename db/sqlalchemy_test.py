# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
from unittest import TestCase, main, mock

from sqlalchemy import func, select

from ._init import closeDb
from ._testDbConfig import testEnv
from ._testHelpers import setup_test_db
from .models import Command


@mock.patch.dict(os.environ, testEnv)
class Test_sqlalchemy(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        cls.session = setup_test_db()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def test_should_connect_and_query(self):
        count = self.session.scalar(select(func.count()).select_from(Command))
        self.assertIsInstance(count, int)


if __name__ == '__main__':
    main()
