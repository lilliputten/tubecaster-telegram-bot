# import sys
# IS_TEST = 'unittest' in sys.modules.keys()
# if not IS_TEST:

from ._collectStats import collectStats
from ._getCurrentMonthStats import getCurrentMonthStats
from ._getMonthlyStats import getMonthlyStats
from ._getTotalStats import getTotalStats
from ._updateStats import updateStats

__all__ = [
    'collectStats',
    'getCurrentMonthStats',
    'getMonthlyStats',
    'getTotalStats',
    'updateStats',
]
