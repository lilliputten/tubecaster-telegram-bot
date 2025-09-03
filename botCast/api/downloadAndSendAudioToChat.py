# -*- coding:utf-8 -*-

import os
import re
import traceback

import telebot  # pyTelegramBotAPI

from botApp import botApp
from botCore.constants import emojies, stickers
from botCore.helpers import getVideoDetailsStr, replyOrSend
from botCore.types import YtdlOptionsType
from core.helpers.errors import errorToString
from core.helpers.files import sizeofFmt
from core.helpers.time import RepeatedTimer
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, errorTitleStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj
from db import updateStats

from ..config.castConfig import logTraceback
from ..helpers._sendAudioToChat import sendAudioToChat
from ..helpers.cleanFiles import cleanFiles
from ..helpers.downloadAudioFile import downloadAudioFile
from ..helpers.downloadInfo import downloadInfo

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
        videoDuration = videoInfo.get('duration')
        debugItems = {
            'audioFileName': audioFileName,
            'audioSizeFmt': audioSizeFmt,
            'audioSize': audioSize,
            'videoSize': videoInfo.get('filesize'),
            'videoSizeFmt': sizeofFmt(videoInfo.get('filesize')),
            'videoDuration': videoDuration,
            # 'TEST': errorTitleStyle('videoDuration should be equal audioSize!'),
        }
        logItems = [
            titleStyle('downloadAndSendAudioToChat: Audio file has been downloaded'),
            secondaryStyle(debugObj(debugItems)),
        ]
        logContent = '\n'.join(logItems)
        _logger.info(logContent)
        # _logger.info(
        #     f"downloadAndSendAudioToChat: Audio file {audioFileName} (with size: {audioSizeFmt}) has been downloaded"
        # )
        sendAudioToChat(
            chatId=chatId,
            videoInfo=videoInfo,
            rootMessage=rootMessage,
            originalMessage=originalMessage,
            audioFileName=audioFileName,
            cleanUp=cleanUp,
        )
        # Update stats
        updateStats(int(chatId), requests=1, volume=audioSize)
    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error download and send an audio: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('downloadAndSendAudioToChat: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('downloadAndSendAudioToChat: ' + errMsg))
        botApp.edit_message_text(
            chat_id=chatId,
            text=errMsg,
            message_id=rootMessage.id,
        )
        # Update stats
        updateStats(int(chatId), failures=1)
        #  raise Exception(errMsg)
    finally:
        timer.stop()
        botApp.delete_message(chatId, rootSticker.id)
        # Remove temporary files and folders
        if options and cleanUp:
            cleanFiles(options)
