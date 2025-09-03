# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

import os
import traceback
from datetime import date
from random import randrange
from typing import Optional
from unittest import TestCase, main, mock

from prisma.models import MonthlyStats, TotalStats, User

from core.helpers.errors import errorToString

from .._init import closeDb, initDb
from .._testDbConfig import testEnv
from ._updateStats import updateStats


@mock.patch.dict(os.environ, testEnv)
class Test_updateStats(TestCase):
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
                # 'isActive': True,
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

            # First update
            updateStats(userId, requests=1, volume=volume)

            # Check TotalStats
            totalStatsClient = TotalStats.prisma()
            totalStats = totalStatsClient.find_unique(where={'userId': userId})
            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 1)
                self.assertEqual(totalStats.volume, volume)

            # Check MonthlyStats
            monthlyStatsClient = MonthlyStats.prisma()
            monthlyStats = monthlyStatsClient.find_unique(
                where={
                    'userId_year_month': {
                        'userId': userId,
                        'year': year,
                        'month': month,
                    }
                }
            )
            self.assertIsNotNone(monthlyStats)
            if monthlyStats:
                self.assertEqual(monthlyStats.requests, 1)
                self.assertEqual(monthlyStats.volume, volume)

            # Second update
            updateStats(userId, requests=1, volume=volume)

            # Check updated values
            totalStats = totalStatsClient.find_unique(where={'userId': userId})
            self.assertIsNotNone(totalStats)
            if totalStats:
                self.assertEqual(totalStats.requests, 2)
                self.assertEqual(totalStats.volume, volume * 2)

            monthlyStats = monthlyStatsClient.find_unique(
                where={
                    'userId_year_month': {
                        'userId': userId,
                        'year': year,
                        'month': month,
                    }
                }
            )
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
            # Clean up
            if totalStats:
                totalStatsClient = TotalStats.prisma()
                totalStatsClient.delete(where={'userId': totalStats.userId})
            if monthlyStats:
                monthlyStatsClient = MonthlyStats.prisma()
                monthlyStatsClient.delete(
                    where={
                        'userId_year_month': {
                            'userId': monthlyStats.userId,
                            'year': year,
                            'month': month,
                        }
                    }
                )


if __name__ == '__main__':
    main()
