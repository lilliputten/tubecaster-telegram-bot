# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from bot.botApp import botApp


def replyOrSend(text: str, chat: telebot.types.Chat, message: telebot.types.Message | None = None):
    if message:
        botApp.reply_to(message, text)
    else:
        botApp.send_message(chat.id, text)
