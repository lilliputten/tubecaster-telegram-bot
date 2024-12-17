# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from datetime import timedelta
import traceback
import os

from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.logger import getLogger

from bot import botApp
from bot.helpers import replyOrSend

from ..types.YtdlOptionsType import YtdlOptionsType
from ..config.castConfig import logTraceback
from ..helpers.cleanFiles import cleanFiles
from ..helpers.downloadAudioFile import downloadAudioFile
from ..helpers.downloadInfo import downloadInfo

_logger = getLogger('bot/commands/downloadAndSendAudioToChat')


#  def sendAudioPieceToChat()


def downloadAndSendAudioToChat(
    url: str, chatId: str | int, username: str, message: telebot.types.Message | None = None
):
    options: YtdlOptionsType | None = None

    try:
        rootMessage = replyOrSend(botApp, 'Ok, fetching the video details...', chatId, message)
        options, videoInfo = downloadInfo(url, chatId, username)

        filesize = videoInfo.get('filesize')
        filesizeApprox = videoInfo.get('filesize_approx')
        sizeFmt = sizeofFmt(filesize if filesize else filesizeApprox)

        details = ', '.join(
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

        #  infoMsg = f'Going to start downloading the video "{title}" of size ({sizeFmt})...'
        infoMsg = ''.join(
            list(
                filter(
                    None,
                    [
                        'Ok, fetching the audio from the video',
                        f' ({details})' if details else '',
                        '...',
                    ],
                )
            )
        )
        replyOrSend(botApp, infoMsg, chatId, message)

        # Load audio from url...
        audioFile = downloadAudioFile(options, videoInfo)
        if not audioFile:
            raise Exception('Audio file name has not been defined')
        audioSize = os.path.getsize(audioFile)
        audioSizeFmt = sizeofFmt(audioSize)
        _logger.info(
            f'downloadAndSendAudioToChat: Audio file {audioFile} (with size: {audioSizeFmt}) has been downloaded'
        )
        infoMsg = ''.join(
            list(
                filter(
                    None,
                    [
                        'Ok, sending the audio',
                        f' ({audioSizeFmt})' if audioSizeFmt else '',
                        '...',
                    ],
                )
            )
        )
        replyOrSend(botApp, infoMsg, chatId, message)
        with open(audioFile, 'rb') as audio:
            # send_audio params:
            #  chat_id: int | str,
            #  audio: Any | str,
            #  caption: str | None = None,
            #  duration: int | None = None,
            #  performer: str | None = None,
            #  title: str | None = None,
            #  reply_to_message_id: int | None = None,
            #  reply_markup: REPLY_MARKUP_TYPES | None = None,
            #  parse_mode: str | None = None,
            #  disable_notification: bool | None = None,
            #  timeout: int | None = None,
            #  thumbnail: Any | str | None = None,
            #  caption_entities: List[MessageEntity] | None = None,
            #  allow_sending_without_reply: bool | None = None,
            #  protect_content: bool | None = None,
            #  message_thread_id: int | None = None,
            #  thumb: Any | str | None = None,
            #  reply_parameters: ReplyParameters | None = None,
            #  business_connection_id: str | None = None,
            #  message_effect_id: str | None = None,
            #  allow_paid_broadcast: bool | None = None
            caption = videoInfo.get('title')
            botApp.send_audio(
                chatId,
                audio=audio,
                caption=caption,
                performer=videoInfo.get('channel'),
                duration=videoInfo.get('duration'),
                thumb=videoInfo.get('thumbnail'),
            )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error fetching audio file: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('downloadAndSendAudioToChat: Traceback for the following error:' + sTraceback)
        _logger.error('downloadAndSendAudioToChat: ' + errMsg)
        replyOrSend(botApp, errMsg, chatId, message)
        #  raise Exception(errMsg)
    finally:
        # Remove temporary files and folders
        if options:
            cleanFiles(options)
