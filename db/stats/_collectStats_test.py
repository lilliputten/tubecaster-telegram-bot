# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
from random import randrange
from datetime import date
import traceback
from typing import Optional
from prisma.models import User, TotalStats, MonthlyStats

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from .._init import closeDb, initDb
from .._testDbConfig import testEnv

from ._collectStats import collectStats
from ._updateStats import updateStats


@mock.patch.dict(os.environ, testEnv)
class Test_collectStats(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enterClassContext(mock.patch.dict(os.environ, testEnv))
        initDb()

    @classmethod
    def tearDownClass(cls):
        closeDb()

    def setUp(self):
        # Create test user
        userClient = User.prisma()
        userId = randrange(100, 999)
        self.user = userClient.create(
            data={
                'id': userId,
                'userStr': f'Test {userId}',
                'userStatus': {
                    'create': {
                        'userMode': 'PAID',
                    },
                },
            },
            include={
                'userStatus': True,
                'totalStats': True,
                'monthlyStats': True,
            },
        )

    def tearDown(self):
        if self.user:
            userClient = User.prisma()
            userClient.delete(
                where={
                    'id': self.user.id,
                },
            )
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

            # Update stats twice
            updateStats(userId, requests=1, volume=volume)
            updateStats(userId, requests=1, volume=volume)

            # Collect stats
            (totalStats, monthlyStats) = collectStats(userId)

            # Check total
            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 2)
                self.assertEqual(totalStats.volume, volume * 2)

            # Check monthly
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
            # Clean up
            if totalStats:
                totalStatsClient = TotalStats.prisma()
                totalStatsClient.delete(where={'userId': totalStats.userId})
            if monthlyStats:
                monthlyStatsClient = MonthlyStats.prisma()
                for monthly in monthlyStats:
                    monthlyStatsClient.delete(
                        where={
                            'userId_year_month': {
                                'userId': monthly.userId,
                                'year': monthly.year,
                                'month': monthly.month,
                            }
                        }
                    )


if __name__ == '__main__':
    main()
