# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from datetime import timedelta
import traceback
import os
from urllib.request import urlopen

from telebot.types import ReplyParameters

from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.helpers.time import RepeatedTimer
from core.logger import getLogger

from botApp import botApp
from botCore.constants import stickers, emojies
from botCore.helpers import getVideoTags
from botCore.helpers import replyOrSend

from botCore.types import YtdlOptionsType

from ..config.castConfig import logTraceback
from ..utils.prepareYoutubeDate import prepareYoutubeDate
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
    print('updateChatStatus')
    botApp.send_chat_action(chatId, action='upload_document')


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
    rootMessage = replyOrSend(botApp, emojies.waiting + ' Ok, fetching the video details...', chatId, originalMessage)

    # Initally update chat status
    updateChatStatus(chatId)

    # Start update timer
    timer = RepeatedTimer(_timerDelyay, updateChatStatus, chatId)

    # Future thumb urlopen handler
    thumb = None

    # Future options, will be downloaded later
    options: YtdlOptionsType | None = None

    try:
        options, videoInfo = downloadInfo(url, chatId, username)

        filesize = videoInfo.get('filesize')
        filesizeApprox = videoInfo.get('filesize_approx')
        sizeFmt = sizeofFmt(filesize if filesize else filesizeApprox)

        videoDetails = ', '.join(
            list(
                filter(
                    None,
                    [
                        sizeFmt,
                        str(timedelta(seconds=int(videoInfo['duration']))) if videoInfo.get('duration') else None,
                        videoInfo.get('resolution'),  # '640x360'
                        str(videoInfo.get('fps')) + ' fps' if videoInfo.get('fps') else None,
                    ],
                )
            )
        )
        infoContent = ''.join(
            list(
                filter(
                    None,
                    [
                        emojies.waiting + ' Ok, extracting an audio from the video',
                        f' ({videoDetails})' if videoDetails else '',
                        '...',
                    ],
                )
            )
        )
        botApp.edit_message_text(
            chat_id=chatId,
            text=infoContent,
            message_id=rootMessage.id,
        )

        # Load audio from url...
        audioFile = downloadAudioFile(options, videoInfo)
        if not audioFile:
            raise Exception('Audio file name has not been defined')
        audioSize = os.path.getsize(audioFile)
        audioSizeFmt = sizeofFmt(audioSize)
        _logger.info(
            f'downloadAndSendAudioToChat: Audio file {audioFile} (with size: {audioSizeFmt}) has been downloaded'
        )
        infoContent = ''.join(
            list(
                filter(
                    None,
                    [
                        emojies.waiting + ' Ok, sending the audio',
                        f' ({audioSizeFmt})' if audioSizeFmt else '',
                        ', extracted from the video',
                        f' ({videoDetails})' if videoDetails else '',
                        '...',
                    ],
                )
            )
        )
        #  replyOrSend(botApp, infoContent, chatId, originalMessage)
        botApp.edit_message_text(
            chat_id=chatId,
            text=infoContent,
            message_id=rootMessage.id,
        )
        with open(audioFile, 'rb') as audio:
            # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.send_audio
            title = videoInfo.get('title')
            captionTitle = ' '.join(
                list(
                    filter(
                        None,
                        [
                            emojies.success,
                            'The audio',
                            f'({audioSizeFmt})' if audioSizeFmt else '',
                            'has been extracted from the video',
                            f'({videoDetails})' if videoDetails else '',
                        ],
                    )
                )
            )
            infoContent = '\n'.join(
                list(
                    filter(
                        None,
                        [
                            # fmt: off
                            'Title: %s' % videoInfo.get('title'),
                            'Link: %s' % videoInfo.get('webpage_url'),
                            'Channel: %s' % videoInfo.get('channel'),  # '进出口服务（AHUANG）'
                            'Duration: %s' % timedelta(seconds=int(videoInfo['duration'])) if videoInfo.get('duration') else None,
                            'Audio size: %s' % audioSizeFmt,
                            'Video size: %s' % sizeFmt,
                            'Upload date: %s' % prepareYoutubeDate(videoInfo.get('upload_date')),  # '20160511'
                            'Tags: %s' % ', '.join(videoInfo['tags']) if videoInfo.get('tags') else None,  # [...]
                            #  'Categories: %s' % ', '.join(videoInfo['categories']) if videoInfo.get('categories') else None,  # [...]
                            #  'Comments count: %s' % videoInfo.get('comment_count'),
                            'Views count: %s' % videoInfo.get('view_count'),
                            #  'Audio channels: %s' % videoInfo.get('audio_channels'),  # 2
                            'Language: %s' % videoInfo.get('language'),  # 'ru' ???
                            # fmt: on
                        ],
                    )
                )
            )
            tagsContent = getVideoTags(videoInfo)
            captionContent = '\n\n'.join(
                list(
                    filter(
                        None,
                        [
                            captionTitle,
                            infoContent,
                            tagsContent,
                        ],
                    )
                )
            )
            thumbnail = videoInfo.get('thumbnail')
            if thumbnail:
                # It'll be closed in the 'finally' section below
                thumb = urlopen(thumbnail)
            botApp.send_audio(
                chatId,
                audio=audio,
                caption=captionContent,
                title=title,
                performer=videoInfo.get('channel'),
                duration=videoInfo.get('duration'),
                thumbnail=thumb,  # videoInfo.get('thumbnail'),
                reply_parameters=ReplyParameters(chat_id=chatId, message_id=originalMessage.id)
                if originalMessage
                else None,
            )
            botApp.delete_message(chatId, rootMessage.id)
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
        if thumb:
            thumb.close()
        botApp.delete_message(chatId, rootSticker.id)
        # Remove temporary files and folders
        if options and cleanUp:
            cleanFiles(options)
