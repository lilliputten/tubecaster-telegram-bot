import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from .downloadAndSendAudioToChat import downloadAndSendAudioToChat
    from .sendInfoToChat import sendInfoToChat

    __all__ = [
        'downloadAndSendAudioToChat',
        'sendInfoToChat',
    ]
