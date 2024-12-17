# -*- coding:utf-8 -*-

from time import sleep
import telebot  # pyTelegramBotAPI
from datetime import timedelta
import traceback

from core.helpers.files import sizeofFmt
from core.helpers.errors import errorToString
from core.helpers.time import RepeatedTimer
from core.logger import getLogger
from core.utils import debugObj

from bot import botApp
from bot.constants import stickers, emojies
from bot.helpers import replyOrSend

from ..config.castConfig import logTraceback
from ..helpers.cleanFiles import cleanFiles
from ..helpers.downloadInfo import downloadInfo
from ..utils.prepareYoutubeDate import prepareYoutubeDate
from ..types.YtdlOptionsType import YtdlOptionsType


_logger = getLogger('bot/cast/sendInfoToChat')

_timerDelyay = 5


def updateChatStatus(chatId: str | int):
    """
    Periodically update chat status.
    """
    print('updateChatStatus')
    botApp.send_chat_action(chatId, action='upload_document')


def sendInfoToChat(url: str, chatId: str | int, username: str, originalMessage: telebot.types.Message | None = None):
    """
    Send info for passed video url.

    Parameters:

    - url: str - Video url.
    - chatId: str | int - Chat id (optional).
    - username: str - Chat username.
    - originalMessage: telebot.types.Message | None = None - Original message reply to (optional).

    Use this small video for test:

    /info https://www.youtube.com/watch?v=EngW7tLk6R8
    """
    options: YtdlOptionsType | None = None

    # Send initial sticker (will be removed) and message (will be updated)
    rootSticker = botApp.send_sticker(chatId, sticker=stickers.typingMrCat)
    rootMessage = replyOrSend(botApp, emojies.waiting + ' Ok, fetching the video details...', chatId, originalMessage)

    # Initally update chat status
    updateChatStatus(chatId)

    # Start update timer
    timer = RepeatedTimer(_timerDelyay, updateChatStatus, chatId)

    try:
        options, videoInfo = downloadInfo(url, chatId, username)
        filesize = videoInfo.get('filesize')
        filesizeApprox = videoInfo.get('filesize_approx')
        sizeFmt = sizeofFmt(filesize if filesize else filesizeApprox)
        debugData = {
            'Link': videoInfo.get('webpage_url'),
            'Title': videoInfo.get('title'),
            #  'Description': videoInfo.get('description'),
            'Channel': videoInfo.get('channel'),  # '进出口服务（AHUANG）'
            'Channel link': videoInfo.get('channel_url'),  # 'https://www.youtube.com/channel/UCslZQaLM_VNzwTzr4SAonqw'
        }
        infoData = {
            #  'Link': videoInfo.get('webpage_url'),
            #  'Title': videoInfo.get('title'),
            #  'Description': videoInfo.get('description'),
            'Duration': timedelta(seconds=int(videoInfo['duration'])) if videoInfo.get('duration') else None,
            'Upload date': prepareYoutubeDate(videoInfo.get('upload_date')),  # '20160511'
            'Release year': videoInfo.get('release_year'),  # None
            'Tags': ', '.join(videoInfo['tags']) if videoInfo.get('tags') else None,  # [...]
            'Categories': ', '.join(videoInfo['categories']) if videoInfo.get('categories') else None,  # [...]
            'Comments count': videoInfo.get('comment_count'),
            'Views count': videoInfo.get('view_count'),
            'File size': sizeFmt,
            'Audio channels': videoInfo.get('audio_channels'),  # 2
            #  'Channel': videoInfo.get('channel'),  # '进出口服务（AHUANG）'
            #  'Channel link': videoInfo.get('channel_url'),  # 'https://www.youtube.com/channel/UCslZQaLM_VNzwTzr4SAonqw'
            'Format note': videoInfo.get('format_note'),  # '360p'
            'Format': videoInfo.get('format'),  # '18 - 640x360 (360p)'
            'Width': videoInfo.get('width'),  # 640
            'Height': videoInfo.get('height'),  # 360
            'Aspect ratio': videoInfo.get('aspect_ratio'),  # 1.78
            'FPS': videoInfo.get('fps'),  # 25
            'Resolution': videoInfo.get('resolution'),  # '640x360'
            'Language': videoInfo.get('language'),  # 'ru' ???
            'Video codec': videoInfo.get('vcodec'),  # 'avc1.42001E'
            'Audio codec': videoInfo.get('acodec'),  # 'mp4a.40.2'
        }
        debugStr = debugObj(debugData)
        infoStr = debugObj(infoData)
        infoContent = '\n\n'.join(
            list(
                filter(
                    None,
                    [
                        emojies.success + ' Video details:',
                        'Title: %s' % videoInfo.get('title'),
                        'Link: %s' % videoInfo.get('webpage_url'),
                        'Channel: %s' % videoInfo.get('channel'),  # '进出口服务（AHUANG）'
                        'Channel link: %s'
                        % videoInfo.get('channel_url'),  # 'https://www.youtube.com/channel/UCslZQaLM_VNzwTzr4SAonqw'
                        #  'Description:\n\n%s' % str(videoInfo.get('description')) if videoInfo.get('description') else None,
                        'Other parameters:',
                        infoStr,
                        #  debugData,
                    ],
                )
            )
        )
        logContent = '\n'.join(['sendInfoToChat', debugStr, infoStr])
        _logger.info(logContent)
        #  replyOrSend(botApp, infoContent, chatId, originalMessage)
        botApp.edit_message_text(
            chat_id=chatId,
            text=infoContent,
            message_id=rootMessage.id,
        )
        if options:
            cleanFiles(options)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error fetching audio info: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('sendInfoToChat: Traceback for the following error:' + sTraceback)
        _logger.error('sendInfoToChat: ' + errMsg)
        #  replyOrSend(botApp, errMsg, chatId, originalMessage)
        botApp.edit_message_text(
            chat_id=chatId,
            text=emojies.error + ' ' + errMsg,
            message_id=rootMessage.id,
        )
        #  raise Exception(errMsg)
    finally:
        timer.stop()
        botApp.delete_message(chatId, rootSticker.id)
        # Remove temporary files and folders
        if options:
            cleanFiles(options)
