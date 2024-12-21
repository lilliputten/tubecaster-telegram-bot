import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from .botRoutes import botRoutes

    from . import (
        _webhookRoute,
        _rootRoute,
        _testRoute,
        _startRoute,
        _stopRoute,
    )

    __all__ = [
        'botRoutes',
        # The rest are only for internal usage only
        '_webhookRoute',
        '_testRoute',
        '_startRoute',
        '_stopRoute',
        '_rootRoute',
    ]
