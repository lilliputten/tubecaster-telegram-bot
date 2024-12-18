# -*- coding:utf-8 -*-

from datetime import timedelta
import telebot  # pyTelegramBotAPI
from telebot.types import ReplyParameters
import math
from urllib.request import urlopen

from core.ffmpeg import probe
from core.helpers.files import getFormattedFileSize
from core.helpers.runtime import getModPath
from core.logger import getLogger

from botApp import botApp
from botCore.helpers import (
    getVideoDetailsStr,
    createVideoCaptionStr,
)
from botCore.types import TVideoInfo
from botCore.constants import emojies


_logger = getLogger(getModPath())   # 'botCast/helpers/_sendAudioPiece')


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
    probeData = probe(audioFileName)
    format = probeData.get('format', {})
    durationPrecise = float(format.get('duration', '0'))   # 1.811156
    duration = round(durationPrecise)
    durationFmt = str(timedelta(seconds=duration))
    # Video details...
    videoDetails = getVideoDetailsStr(videoInfo)
    pieceInfo = f' {pieceNo + 1}/{piecesCount}' if pieceNo != None and piecesCount else None
    #  # It's a copy of the message from `downloadAndSendAudioToChat`
    #  infoContent = ''.join(
    #      filter(
    #          None,
    #          [
    #              emojies.waiting + ' Extracting an audio',
    #              pieceInfo,
    #              ' from the video',
    #              f' ({videoDetails})' if videoDetails else '',
    #              '...',
    #          ],
    #      )
    #  )
    #  _logger.info(infoContent)
    #  if rootMessage:
    #      botApp.edit_message_text(
    #          chat_id=chatId,
    #          message_id=rootMessage.id,
    #          text=infoContent,
    #      )
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
                duration=duration,  # videoInfo.get('duration'),
                thumbnail=thumb,
                reply_parameters=(
                    ReplyParameters(chat_id=chatId, message_id=originalMessage.id) if originalMessage else None
                ),
            )
            _logger.info(captionContent)
        finally:
            if thumb:
                thumb.close()
