# import sys
# IS_TEST = 'unittest' in sys.modules.keys()
# if not IS_TEST:

from ._getUserStatus import getUserStatus
from ._updateUserStatus import updateUserStatus

__all__ = [
    'getUserStatus',
    'updateUserStatus',
]
