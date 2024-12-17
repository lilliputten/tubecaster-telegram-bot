# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
import traceback
from urllib.request import urlopen

from telebot.types import ReplyParameters

from core.helpers.files import getFormattedFileSize
from core.helpers.errors import errorToString
from core.helpers.time import RepeatedTimer
from core.logger import getLogger

from botApp import botApp
from botCore.helpers import (
    replyOrSend,
    getVideoDetailsStr,
    createVideoCaptionStr,
)
from botCore.types import YtdlOptionsType, TVideoInfo
from botCore.constants import stickers, emojies

from ..config.castConfig import logTraceback
from ..helpers.cleanFiles import cleanFiles
from ..helpers.downloadAudioFile import downloadAudioFile
from ..helpers.downloadInfo import downloadInfo

_logger = getLogger('botCast/downloadAndSendAudioToChat')

_timerDelyay = 5

#  def sendAudioPieceToChat()


def updateChatStatus(chatId: str | int):
    """
    Periodically update chat status.
    """
    _logger.info(f'updateChatStatus')
    botApp.send_chat_action(chatId, action='upload_document')


def sendAudioPiece(
    audioFileName: str,
    chatId: str | int,
    rootMessage: telebot.types.Message,
    videoInfo: TVideoInfo,
    originalMessage: telebot.types.Message | None = None,
    pieceNo: int | None = None,
    piecesCount: int | None = None,
):
    videoDetails = getVideoDetailsStr(videoInfo)
    pieceInfo = f' {pieceNo + 1}/{piecesCount}' if pieceNo != None and piecesCount else None
    infoContent = ''.join(
        filter(
            None,
            [
                emojies.waiting + ' Extracting an audio',
                pieceInfo,
                'from the video',
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
    audioSizeFmt = getFormattedFileSize(audioFileName)
    infoContent = ''.join(
        filter(
            None,
            [
                emojies.waiting + ' Sending the audio',
                pieceInfo,
                f' ({audioSizeFmt})' if audioSizeFmt else '',
                ', extracted from the video',
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
    with open(audioFileName, 'rb') as audio:
        # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.send_audio
        title = videoInfo.get('title')
        captionContent = createVideoCaptionStr(
            videoInfo=videoInfo,
            audioFileName=audioFileName,
            pieceNo=pieceNo,
            piecesCount=piecesCount,
        )
        thumbnail = videoInfo.get('thumbnail')
        # Future thumb urlopen handler
        thumb = None
        if thumbnail:
            # It'll be closed in the 'finally' section below
            thumb = urlopen(thumbnail)
        try:
            botApp.send_audio(
                chatId,
                audio=audio,
                caption=captionContent,
                title=title,
                performer=videoInfo.get('channel'),
                duration=videoInfo.get('duration'),
                thumbnail=thumb,
                reply_parameters=(
                    ReplyParameters(chat_id=chatId, message_id=originalMessage.id) if originalMessage else None
                ),
            )
            botApp.delete_message(chatId, rootMessage.id)
        finally:
            if thumb:
                thumb.close()


def downloadAndSendAudioToChat(
    url: str,
    chatId: str | int,
    username: str,
    originalMessage: telebot.types.Message | None = None,
    cleanUp: bool | None = True,
):
    """
    Send info for passed video url.

    Parameters:

    - url: str - Video url.
    - chatId: str | int - Chat id (optional).
    - username: str - Chat username.
    - originalMessage: telebot.types.Message | None = None - Original message reply to (optional).
    - cleanUp: bool | None = False - Cleann all the temporarily and generated files at the end (true by default).

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
    timer = RepeatedTimer(_timerDelyay, updateChatStatus, chatId)

    #  # Future thumb urlopen handler
    #  thumb = None

    # Future options, will be downloaded later
    options: YtdlOptionsType | None = None

    try:
        options, videoInfo = downloadInfo(url, chatId, username)

        videoDetails = getVideoDetailsStr(videoInfo)
        infoContent = ''.join(
            filter(
                None,
                [
                    emojies.waiting + ' Extracting an audio from the video',
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
        audioSizeFmt = getFormattedFileSize(audioFileName)
        _logger.info(
            f'downloadAndSendAudioToChat: Audio file {audioFileName} (with size: {audioSizeFmt}) has been downloaded'
        )
        sendAudioPiece(
            audioFileName=audioFileName,
            chatId=chatId,
            rootMessage=rootMessage,
            videoInfo=videoInfo,
            originalMessage=originalMessage,
            pieceNo=0,
            piecesCount=3,
        )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error downloading an audio file: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('downloadAndSendAudioToChat: Traceback for the following error:' + sTraceback)
        _logger.error('downloadAndSendAudioToChat: ' + errMsg)
        #  replyOrSend(botApp, errMsg, chatId, originalMessage)
        botApp.edit_message_text(
            chat_id=chatId,
            text=errMsg,
            message_id=rootMessage.id,
        )
        #  raise Exception(errMsg)
    finally:
        timer.stop()
        #  if thumb:
        #      thumb.close()
        botApp.delete_message(chatId, rootSticker.id)
        # Remove temporary files and folders
        if options and cleanUp:
            cleanFiles(options)
