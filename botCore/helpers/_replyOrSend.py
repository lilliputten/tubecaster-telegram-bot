# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types

from botApp import botApp


def replyOrSend(text: str, chatId: int | str, message: types.Message | None = None):
    if message:
        return botApp.reply_to(message, text)
    else:
        return botApp.send_message(chatId, text)
