import sys

IS_TEST = 'unittest' in sys.modules.keys()
if not IS_TEST:
    from .api import downloadAndSendAudioToChat, sendInfoToChat, sendStatsToChat
    from .config import castConfig

    __all__ = [
        'castConfig',
        'downloadAndSendAudioToChat',
        'sendInfoToChat',
        'sendStatsToChat',
    ]
