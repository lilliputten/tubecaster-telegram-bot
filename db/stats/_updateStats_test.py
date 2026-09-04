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
from ._updateStats import updateStats


@mock.patch.dict(os.environ, testEnv)
class Test_updateStats(TestCase):
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

    def test_updateStats_should_create_and_update_total_and_monthly_stats(self):
        totalStats: Optional[TotalStats] = None
        monthlyStats: Optional[MonthlyStats] = None
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        try:
            if not self.user:
                self.fail('User not created')

            userId = self.user.id
            volume = 500

            updateStats(userId, requests=1, volume=volume)

            session = initDb()
            totalStats = session.get(TotalStats, userId)
            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 1)
                self.assertEqual(totalStats.volume, volume)

            monthlyStats = session.get(MonthlyStats, (userId, year, month))
            self.assertIsNotNone(monthlyStats)
            if monthlyStats:
                self.assertEqual(monthlyStats.requests, 1)
                self.assertEqual(monthlyStats.volume, volume)

            updateStats(userId, requests=1, volume=volume)

            totalStats = session.get(TotalStats, userId)
            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 2)
                self.assertEqual(totalStats.volume, volume * 2)

            monthlyStats = session.get(MonthlyStats, (userId, year, month))
            self.assertIsNotNone(monthlyStats)
            if monthlyStats:
                self.assertEqual(monthlyStats.requests, 2)
                self.assertEqual(monthlyStats.volume, volume * 2)
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
                db_monthly = session.get(MonthlyStats, (monthlyStats.userId, year, month))
                if db_monthly:
                    session.delete(db_monthly)
                    session.commit()


if __name__ == '__main__':
    main()
