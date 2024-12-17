# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def createCommonButtonsMarkup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    castItem = telebot.types.InlineKeyboardButton('Cast video', callback_data='startCast')
    helpItem = telebot.types.InlineKeyboardButton('Show help', callback_data='startHelp')
    markup.add(castItem, helpItem)
    return markup
