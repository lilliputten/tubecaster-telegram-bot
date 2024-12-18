import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from .botRoutes import botRoutes

    from . import _allRoutes, _webhookRoute

    __all__ = [
        'botRoutes',
        # The rest are only for internal usage only
        '_allRoutes',
        '_webhookRoute',
    ]
