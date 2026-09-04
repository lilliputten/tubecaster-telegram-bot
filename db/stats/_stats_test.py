# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
import traceback
from datetime import date
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from .._init import closeDb, initDb
from .._testDbConfig import testEnv
from .._testHelpers import setup_test_db
from ..models import MonthlyStats, TotalStats, User


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
        userId = randrange(100, 999)
        self.user = User(id=userId, userStr=f'Test {userId}')
        session.add(self.user)
        session.commit()

    def tearDown(self):
        if self.user:
            session = initDb()
            user = session.get(User, self.user.id)
            if user:
                session.delete(user)
                session.commit()
            self.user = None

    def test_should_add_monthly_stats_record(self):
        monthlyStats: Optional[MonthlyStats] = None
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        try:
            session = initDb()
            if self.user:
                monthlyStats = MonthlyStats(
                    userId=self.user.id,
                    year=year,
                    month=month,
                    requests=1,
                    volume=100,
                )
                session.add(monthlyStats)
                session.commit()
            self.assertIsInstance(monthlyStats, MonthlyStats)
            if monthlyStats:
                self.assertIsInstance(monthlyStats.userId, int)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if monthlyStats:
                session = initDb()
                db_stats = session.get(MonthlyStats, (monthlyStats.userId, year, month))
                if db_stats:
                    session.delete(db_stats)
                    session.commit()

    def test_should_add_total_stats_record(self):
        totalStats: Optional[TotalStats] = None
        try:
            session = initDb()
            if self.user:
                totalStats = TotalStats(
                    userId=self.user.id,
                    requests=1,
                    volume=100,
                )
                session.add(totalStats)
                session.commit()
            self.assertIsInstance(totalStats, TotalStats)
            if totalStats:
                self.assertIsInstance(totalStats.userId, int)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            if totalStats:
                session = initDb()
                db_stats = session.get(TotalStats, totalStats.userId)
                if db_stats:
                    session.delete(db_stats)
                    session.commit()


if __name__ == '__main__':
    main()
