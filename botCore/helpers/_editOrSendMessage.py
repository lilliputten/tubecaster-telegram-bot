# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp


def editOrSendMessage(text: str, chatId: int | str, message: telebot.types.Message | None = None):
    try:
        if not message:
            raise Exception('No message')
        botApp.edit_message_text(
            chat_id=chatId,
            text=text,
            message_id=message.id,
        )
    except:
        botApp.send_message(
            chat_id=chatId,
            text=text,
        )
