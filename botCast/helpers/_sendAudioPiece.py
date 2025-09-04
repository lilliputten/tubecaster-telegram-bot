# -*- coding:utf-8 -*-

import math
import traceback
from datetime import timedelta
from urllib.request import urlopen

import telebot  # pyTelegramBotAPI
from telebot.types import ReplyParameters

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import createVideoCaptionStr, getVideoDetailsStr
from botCore.types import TVideoInfo
from core.ffmpeg import probe, probeDuration
from core.helpers.errors import errorToString
from core.helpers.files import getFormattedFileSize
from core.helpers.strings import truncStr
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle

_logger = getDebugLogger()   # 'botCast/helpers/_sendAudioPiece')

logTraceback = False


def sendAudioPiece(
    chatId: str | int,
    videoInfo: TVideoInfo,
    rootMessage: telebot.types.Message | None = None,
    originalMessage: telebot.types.Message | None = None,
    audioFileName: str = '',
    pieceNo: int | None = None,
    piecesCount: int | None = None,
):
    # Get audio duration (via ffmpeg probe)...
    # probeData = probe(audioFileName)
    # format = probeData.get('format', {})
    # durationPrecise = float(format.get('duration', '0'))   # 1.811156
    # duration = round(durationPrecise)
    duration = probeDuration(audioFileName)
    durationFmt = str(timedelta(seconds=round(duration)))
    # Video details...
    videoDetails = getVideoDetailsStr(videoInfo)
    pieceInfo = f' {pieceNo + 1}/{piecesCount}' if pieceNo != None and piecesCount and piecesCount > 1 else None
    audioSizeFmt = getFormattedFileSize(audioFileName)
    infoContent = ''.join(
        filter(
            None,
            [
                emojies.waiting + ' Sending the audio',
                pieceInfo,
                f' ({durationFmt}, {audioSizeFmt})' if audioSizeFmt else '',
                ', extracted from the video',
                f' ({videoDetails})' if videoDetails else '',
                '...',
            ],
        )
    )
    _logger.info(infoContent)
    if rootMessage:
        botApp.edit_message_text(
            chat_id=chatId,
            message_id=rootMessage.id,
            text=infoContent,
        )
    else:
        botApp.send_message(
            chat_id=chatId,
            text=infoContent,
        )
    with open(audioFileName, 'rb') as audio:
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
            # TODO: To load a thumbnail only once, in the parent wrapper?
        try:
            botApp.send_audio(
                # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.send_audio
                chatId,
                audio=audio,
                caption=captionContent,
                title=title,
                performer=videoInfo.get('channel'),
                duration=int(duration),
                thumbnail=thumb,
                reply_parameters=(
                    ReplyParameters(chat_id=chatId, message_id=originalMessage.id) if originalMessage else None
                ),
            )
            _logger.info(captionContent)
        except Exception as err:
            errText = truncStr(errorToString(err, show_stacktrace=False), 100)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = emojies.error + ' Error sending an audio file to the chat: ' + errText
            if logTraceback:
                errMsg += sTraceback
            else:
                _logger.warning(warningStyle('logTraceback: Traceback for the following error:') + sTraceback)
            _logger.error(errorStyle('logTraceback: ' + errMsg))
            raise Exception(errMsg)
        finally:
            if thumb:
                thumb.close()
