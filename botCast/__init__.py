import sys
IS_TEST = 'unittest' in sys.modules.keys()
if not IS_TEST:
    from .api.sendInfoToChat import sendInfoToChat
    from .api.downloadAndSendAudioToChat import downloadAndSendAudioToChat
    from .config import castConfig
    __all__ = [
        'sendInfoToChat',
        'downloadAndSendAudioToChat',
        'castConfig',
    ]
