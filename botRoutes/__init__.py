import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from . import _rootRoute, _startRoute, _stopRoute, _testRoute, _webhookRoute
    from .botRoutes import botRoutes

    __all__ = [
        'botRoutes',
        # The rest are only for internal usage only
        '_webhookRoute',
        '_testRoute',
        '_startRoute',
        '_stopRoute',
        '_rootRoute',
    ]
