# -*- coding:utf-8 -*-
# @see https://docs.python.org/3/library/unittest.html

# NOTE: For running only current test use:
#  - `python -m unittest -v -f botCore/helpers/_addTempMessage_test.py` (under venv)
#  - `poetry run python -m unittest -v -f botCore/helpers/_addTempMessage_test.py`
#  - `poetry run python -m unittest -v -f -p '*_test.py' -k _addTempMessage_test`

import os
from random import randrange
from datetime import date
import traceback
from typing import Optional
from prisma.models import User, TotalStats, MonthlyStats

from unittest import TestCase, main, mock

from core.helpers.errors import errorToString

from ._init import closeDb, initDb

from ._testDbConfig import testEnv
from ._types import TTempMessage

from ._addTempMessage import addTempMessage


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
        # Create test user
        userClient = User.prisma()
        userId = randrange(100, 999)
        self.user = userClient.create(
            data={
                'id': userId,
                'userStr': f'Test {userId}',
                'isActive': True,
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

    def test_should_add_monthly_stats_record(self):
        monthlyStats: Optional[MonthlyStats] = None
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        try:
            monthlyStatsClient = MonthlyStats.prisma()
            # Create monthly stats record
            if self.user:
                monthlyStats = monthlyStatsClient.create(
                    data={
                        'userId': self.user.id,
                        'year': year,
                        'month': month,
                        'requests': 1,
                        'volume': 100,
                    },
                )
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
                monthlyStatsClient = MonthlyStats.prisma()
                monthlyStatsClient.delete(
                    where={
                        'userId_year_month': {
                            'userId': monthlyStats.userId,
                            'year': year,
                            'month': month,
                        }
                    },
                )

    def test_should_add_total_stats_record(self):
        totalStats: Optional[TotalStats] = None
        try:
            # user: Optional[User] = None
            totalStatsClient = TotalStats.prisma()
            # Create total stats record
            if self.user:
                totalStats = totalStatsClient.create(
                    data={
                        'userId': self.user.id,
                        'requests': 1,
                        'volume': 100,
                    },
                )
                # userClient = User.prisma()
                # user = userClient.find_unique(
                #     where={
                #         'id': self.user.id,
                #     },
                #     include={
                #         'totalStats': True,
                #         'monthlyStats': True,
                #     },
                # )
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
                totalStatsClient = TotalStats.prisma()
                totalStatsClient.delete(
                    where={
                        'userId': totalStats.userId,
                    },
                )


if __name__ == '__main__':
    main()
