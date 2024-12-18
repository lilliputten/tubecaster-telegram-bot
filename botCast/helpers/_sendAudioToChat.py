# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
import os
import traceback
from functools import partial

from core.appConfig import MAX_AUDIO_FILE_SIZE
from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.helpers.runtime import getModPath
from core.logger import getLogger

from botApp import botApp
from botCore.types import TVideoInfo
from botCore.constants import emojies
from botCore.helpers import (
    getDesiredPiecesCount,
)
from botCore.routines import splitAudio

from ..config.castConfig import logTraceback
from ..helpers._sendAudioPiece import sendAudioPiece


_logger = getLogger(getModPath())


def sendAudioToChat(
    chatId: str | int,
    videoInfo: TVideoInfo,
    rootMessage: telebot.types.Message | None = None,
    originalMessage: telebot.types.Message | None = None,
    audioFileName: str = '',
    cleanUp: bool = True,
    maxAudioFileSize: int = MAX_AUDIO_FILE_SIZE,
    splitGap: int = 1,
):
    try:
        audioSize = os.path.getsize(audioFileName)
        audioSizeFmt = sizeofFmt(audioSize)
        pieceCallback = partial(
            sendAudioPiece,
            chatId,
            videoInfo,
            rootMessage,
            originalMessage,
        )
        useSplit = True
        if useSplit and audioSize >= maxAudioFileSize:
            # File is too large, send it by pieces...
            piecesCount = getDesiredPiecesCount(audioSize, maxAudioFileSize)
            outFilePrefix = audioFileName + '-part'
            infoMsg = (
                emojies.waiting
                + f' The audio file size of {audioSizeFmt} exceeds the Telegram API limit of {sizeofFmt(maxAudioFileSize)} and will be divided into {piecesCount} parts...'
            )
            if rootMessage:
                botApp.edit_message_text(
                    chat_id=chatId,
                    text=infoMsg,
                    message_id=rootMessage.id,
                )
            _logger.info('downloadAndSendAudioToChat: %s' % infoMsg)
            splitAudio(
                audioFileName=audioFileName,
                outFilePrefix=outFilePrefix,
                piecesCount=piecesCount,
                pieceCallback=pieceCallback,
                #  delimiter=delimiter,
                gap=splitGap,
                removeFiles=cleanUp,
            )
        else:
            # Send whole file...
            pieceCallback(
                audioFileName=audioFileName,
            )
        if rootMessage:
            botApp.delete_message(chatId, rootMessage.id)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error sending an audio file to the chat: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('sendAudioToChat: Traceback for the following error:' + sTraceback)
        _logger.error('sendAudioToChat: ' + errMsg)
        raise Exception(errMsg)
