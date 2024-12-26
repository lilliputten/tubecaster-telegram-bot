# -*- coding:utf-8 -*-

from datetime import timedelta
import re
from typing import Optional
import telebot  # pyTelegramBotAPI
import os
import traceback
from functools import partial

from core.appConfig import AUDIO_FILE_EXT, MAX_AUDIO_FILE_SIZE
from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString

from core.logger import getDebugLogger
from core.logger.utils import errorStyle, errorTitleStyle, warningStyle, secondaryStyle, primaryStyle, titleStyle
from core.utils import debugObj

from botApp import botApp
from botCore.types import TVideoInfo
from botCore.constants import emojies
from botCore.helpers import getDesiredPiecesCount
from botCore.routines import splitAudio

from ..config.castConfig import logTraceback
from ..helpers._sendAudioPiece import sendAudioPiece


_logger = getDebugLogger()


def sendAudioToChat(
    chatId: str | int,
    videoInfo: TVideoInfo,
    rootMessage: telebot.types.Message | None = None,
    originalMessage: telebot.types.Message | None = None,
    audioFileName: str = '',
    cleanUp: bool = True,
    maxAudioFileSize: int | None = MAX_AUDIO_FILE_SIZE,
    splitGap: int = 1,
    delimiter: str = '-',
):
    newMessage: Optional[telebot.types.Message] = None
    try:
        audioSize = os.path.getsize(audioFileName)
        audioSizeFmt = sizeofFmt(audioSize)
        # Prepare a callback send an audio fragment
        sendAudioPieceCallback = partial(
            sendAudioPiece,
            chatId,
            videoInfo,
            rootMessage,
            originalMessage,
        )
        isOversized = audioSize >= maxAudioFileSize if maxAudioFileSize else False

        # if isOversized:  # File is too large, send it by pieces...

        piecesCount = getDesiredPiecesCount(audioSize, maxAudioFileSize)
        outFilePrefix = audioFileName
        if outFilePrefix.endswith(AUDIO_FILE_EXT):
            outFilePrefix = outFilePrefix[: len(outFilePrefix) - len(AUDIO_FILE_EXT)]
        outFilePrefix += delimiter + ('part' if piecesCount > 1 else 'ready')
        infoMsg = (
            (
                emojies.waiting
                + ' '
                + f'The audio file size of {audioSizeFmt} exceeds the Telegram API limit of {sizeofFmt(maxAudioFileSize)} and will be divided into {piecesCount} parts...'
            )
            if isOversized
            else (emojies.waiting + ' ' + f'Sending audio of size {audioSizeFmt}...')
        )
        if isOversized:
            newMessage = botApp.send_message(
                chat_id=chatId,
                text=infoMsg,
            )
        _logger.info('downloadAndSendAudioToChat: %s' % infoMsg)

        # Show debug info
        videoDuration = videoInfo.get('duration')
        debugItems = {
            'infoMsg': infoMsg,
            'isOversized': isOversized,
            'piecesCount': piecesCount,
            'outFilePrefix': outFilePrefix,
            'audioFileName': audioFileName,
            'audioSizeFmt': audioSizeFmt,
            'audioSize': audioSize,
            'videoSize': videoInfo.get('filesize'),
            'videoSizeFmt': sizeofFmt(videoInfo.get('filesize')),
            'videoDuration': videoDuration,
            'videoDurationFmt': timedelta(seconds=float(videoDuration)) if videoDuration else None,
            'TEST': errorTitleStyle(
                'Issue #34: videoDuration should be equal audioDuration (see next log output, from splitAudio)!'
            ),
        }
        logItems = [
            titleStyle('sendAudioToChat: Audio file is ready to send'),
            secondaryStyle(debugObj(debugItems)),
        ]
        logContent = '\n'.join(logItems)
        _logger.debug(logContent)

        splitAudio(
            audioFileName=audioFileName,
            outFilePrefix=outFilePrefix,
            piecesCount=piecesCount,
            pieceCallback=sendAudioPieceCallback,
            delimiter=delimiter,
            gap=splitGap,
            removeFiles=cleanUp,
            duration=videoDuration,  # Issue #34: Pass an actual duration to split audio code
        )

        # else:
        #     # Send whole file...
        #     sendAudioPieceCallback(
        #         audioFileName=audioFileName,
        #     )

        if rootMessage:
            botApp.delete_message(chatId, rootMessage.id)
    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error sending an audio file to the chat: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('sendAudioToChat: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('sendAudioToChat: ' + errMsg))
        raise Exception(errMsg)
    finally:
        if newMessage:
            botApp.delete_message(chat_id=chatId, message_id=newMessage.id)
