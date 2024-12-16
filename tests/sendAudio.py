# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from typing import NewType, TypedDict, Optional, Any, Dict, AnyStr
from datetime import timedelta
import traceback
import re
import os
import posixpath
import pathlib

from core.appConfig import appConfig, CWD_PATH, TEMP_PATH, TELEGRAM_OWNER_ID

from bot import botApp


TVideoInfo = dict[str, Any]


def sendAudio(audioPath: str, chatId: int | str, videoInfo: TVideoInfo):
    with open(audioPath, 'rb') as audio:
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
        botApp.send_audio(
            chatId,
            audio=audio,
            caption=videoInfo.get('title'),
            duration=videoInfo.get('duration'),
            thumb=videoInfo.get('thumbnail'),
        )


if __name__ == '__main__':
    audioFile = 'tests/test-audios/test-short.mp3'
    audioPath = posixpath.join(CWD_PATH, audioFile)
    videoInfo: TVideoInfo = {
        'title': 'Test audio',
    }
    print('Sending audio', audioPath)
    sendAudio(audioPath, chatId=TELEGRAM_OWNER_ID, videoInfo=videoInfo)
