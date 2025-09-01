import sys

IS_TEST = 'unittest' in sys.modules.keys()
if not IS_TEST:
    from .config import castConfig
    from .api import downloadAndSendAudioToChat, sendInfoToChat, sendStatsToChat

    __all__ = [
        'castConfig',
        'downloadAndSendAudioToChat',
        'sendInfoToChat',
        'sendStatsToChat',
    ]
