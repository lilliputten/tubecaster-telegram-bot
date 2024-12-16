# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def replyOrSend(botApp: telebot.TeleBot, text: str, chatId: int | str, message: telebot.types.Message | None = None):
    if message:
        botApp.reply_to(message, text)
    else:
        botApp.send_message(chatId, text)
