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
from ..models import MonthlyStats, TotalStats, User, UserStatus
from ._collectStats import collectStats
from ._updateStats import updateStats


@mock.patch.dict(os.environ, testEnv)
class Test_collectStats(TestCase):
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
        session.flush()
        session.add(UserStatus(userId=userId, userMode='PAID'))
        session.commit()

    def tearDown(self):
        if self.user:
            session = initDb()
            user = session.get(User, self.user.id)
            if user:
                session.delete(user)
                session.commit()
            self.user = None

    def test_collectStats_should_return_total_and_monthly_stats(self):
        totalStats: Optional[TotalStats] = None
        monthlyStats: Optional[list[MonthlyStats]] = None
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        try:
            if not self.user:
                self.fail('User not created')

            userId = self.user.id
            volume = 500

            updateStats(userId, requests=1, volume=volume)
            updateStats(userId, requests=1, volume=volume)

            (totalStats, monthlyStats) = collectStats(userId)

            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 2)
                self.assertEqual(totalStats.volume, volume * 2)

            self.assertIsInstance(monthlyStats, list)
            if monthlyStats:
                self.assertEqual(len(monthlyStats), 1)
                monthly = monthlyStats[0]
                self.assertEqual(monthly.requests, 2)
                self.assertEqual(monthly.volume, volume * 2)
                self.assertEqual(monthly.year, year)
                self.assertEqual(monthly.month, month)

        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error: ' + errText
            print('Traceback for the following error:' + sTraceback)
            print('Error: ' + errMsg)
        finally:
            session = initDb()
            if totalStats:
                db_total = session.get(TotalStats, totalStats.userId)
                if db_total:
                    session.delete(db_total)
                    session.commit()
            if monthlyStats:
                for monthly in monthlyStats:
                    db_monthly = session.get(MonthlyStats, (monthly.userId, monthly.year, monthly.month))
                    if db_monthly:
                        session.delete(db_monthly)
                        session.commit()


if __name__ == '__main__':
    main()
