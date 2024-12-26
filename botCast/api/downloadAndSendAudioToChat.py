# -*- coding:utf-8 -*-

import os
import telebot  # pyTelegramBotAPI
import traceback

from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString

from core.helpers.time import RepeatedTimer
from core.logger import getDebugLogger

from botApp import botApp
from botCore.types import YtdlOptionsType
from botCore.constants import stickers, emojies
from botCore.helpers import (
    replyOrSend,
    getVideoDetailsStr,
)
from core.logger.utils import errorStyle, warningStyle

from ..config.castConfig import logTraceback
from ..helpers.cleanFiles import cleanFiles
from ..helpers.downloadAudioFile import downloadAudioFile
from ..helpers.downloadInfo import downloadInfo
from ..helpers._sendAudioToChat import sendAudioToChat


_logger = getDebugLogger()

_timerDelay = 5


def updateChatStatus(chatId: str | int):
    """
    Periodically update chat status.
    """
    _logger.info(f'updateChatStatus')
    botApp.send_chat_action(chatId, action='upload_document')


def downloadAndSendAudioToChat(
    url: str,
    chatId: str | int,
    username: str,
    originalMessage: telebot.types.Message | None = None,
    cleanUp: bool = True,
):
    """
    Send info for passed video url.

    Parameters:

    - url: str - Video url.
    - chatId: str | int - Chat id (optional).
    - username: str - Chat username.
    - originalMessage: telebot.types.Message | None = None - Original message reply to (optional).
    - cleanUp: bool | None = False - Clean all the temporary and generated files at the end (true by default).

    For tests, use the command:

    /cast https://www.youtube.com/watch?v=EngW7tLk6R8

    Or the test module:

    tests/downloadAndSendAudioToChat.test.py
    """

    # Send initial sticker (will be removed) and message (will be updated)
    rootSticker = botApp.send_sticker(chatId, sticker=stickers.walkingMrCat)
    rootMessage = replyOrSend(botApp, emojies.waiting + ' Fetching the video details...', chatId, originalMessage)

    # Initally update chat status
    updateChatStatus(chatId)

    # Start update timer
    timer = RepeatedTimer(_timerDelay, updateChatStatus, chatId)

    # Future options, will be downloaded later
    options: YtdlOptionsType | None = None

    try:
        options, videoInfo = downloadInfo(url, chatId, username)

        videoDetails = getVideoDetailsStr(videoInfo)
        infoContent = ''.join(
            filter(
                None,
                [
                    emojies.waiting + ' Downloading an audio from the video',
                    f' ({videoDetails})' if videoDetails else '',
                    '...',
                ],
            )
        )
        botApp.edit_message_text(
            chat_id=chatId,
            text=infoContent,
            message_id=rootMessage.id,
        )

        # Load audio from url...
        audioFileName = downloadAudioFile(options, videoInfo)
        if not audioFileName:
            raise Exception('Audio file name has not been defined')
        audioSize = os.path.getsize(audioFileName)
        audioSizeFmt = sizeofFmt(audioSize)
        _logger.info(
            f'downloadAndSendAudioToChat: Audio file {audioFileName} (with size: {audioSizeFmt}) has been downloaded'
        )
        sendAudioToChat(
            chatId=chatId,
            videoInfo=videoInfo,
            rootMessage=rootMessage,
            originalMessage=originalMessage,
            audioFileName=audioFileName,
            cleanUp=cleanUp,
        )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error download and send an audio: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(
                warningStyle(warningStyle('downloadAndSendAudioToChat: Traceback for the following error:'))
                + sTraceback
            )
        _logger.error(errorStyle('downloadAndSendAudioToChat: ' + errMsg))
        botApp.edit_message_text(
            chat_id=chatId,
            text=errMsg,
            message_id=rootMessage.id,
        )
        #  raise Exception(errMsg)
    finally:
        timer.stop()
        botApp.delete_message(chatId, rootSticker.id)
        # Remove temporary files and folders
        if options and cleanUp:
            cleanFiles(options)
