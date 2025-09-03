# -*- coding:utf-8 -*-

import traceback

import telebot  # pyTelegramBotAPI
from prisma.models import MonthlyStats, TotalStats

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import replyOrSend
from core.helpers.errors import errorToString
from core.helpers.files import sizeofFmt
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle, tretiaryStyle, warningTitleStyle
from core.utils import debugObj
from db import collectStats

from ..config.castConfig import logTraceback

_logger = getDebugLogger()


def formatStatsEntry(title: str, stats: TotalStats | MonthlyStats | None):
    if not stats:
        return None
    volume = stats.volume
    volumeFmt = sizeofFmt(volume) if volume else None

    debugData = {
        'title': title,
        'volume': volume,
    }
    infoData = {
        'Downloaded audios': stats.requests,
        'Info requests': stats.infoRequests,
        'Failures': stats.failures,
        'Downloaded volume': volumeFmt,
    }
    debugStr = debugObj(debugData)
    infoStr = debugObj(infoData)
    infoItems = [
        emojies.info + ' ' + title + ':',
        infoStr,
    ]
    infoItems = list(filter(None, infoItems))
    if not len(infoItems):
        return None
    infoContent = '\n\n'.join(infoItems)
    logContent = '\n'.join([titleStyle('formatStatsEntry: ' + title), debugStr, infoStr])
    _logger.info(logContent)

    return infoContent


def sendStatsToChat(
    statsForUserId: int, chatId: str | int, username: str, originalMessage: telebot.types.Message | None = None
):
    """
    Send info for passed video url.

    Parameters:

    - statsForUserId: int - User id to collect the stats for (usually is the current user; but admin can request stats for another user).
    - chatId: str | int - Chat/user id.
    - username: str - Chat username.
    - originalMessage: telebot.types.Message | None = None - Original message reply to (optional).
    """

    try:
        (totalStats, monthlyStats) = collectStats(statsForUserId)

        totalStatsInfo = formatStatsEntry('Total statistics', totalStats)
        infoItems = [
            totalStatsInfo,
        ]
        for statsItem in monthlyStats:
            title = f'{statsItem.year}-{statsItem.month:02d}'
            infoStr = formatStatsEntry(title, statsItem)
            infoItems.append(infoStr)

        debugData = {
            'statsForUserId': statsForUserId,
            'chatId': chatId,
            'username': username,
        }
        debugStr = debugObj(debugData)
        # infoStr = debugObj(infoData)
        # tagsContent = getVideoTags(videoInfo)
        infoItems = list(filter(None, infoItems))
        infoContent = '\n\n'.join(infoItems)
        if not len(infoItems):
            infoContent = emojies.info + ' ' + 'You do not have any usage statistics yet.'
        logContent = '\n'.join([titleStyle('sendStatsToChat'), debugStr, infoContent])
        _logger.info(logContent)
        replyOrSend(botApp, infoContent, chatId, originalMessage)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error collecting stats: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info(
                warningTitleStyle('sendStatsToChat: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
        _logger.error(errorStyle('sendStatsToChat: ' + errMsg))
        replyOrSend(botApp, errMsg, chatId, originalMessage)
        #  raise Exception(errMsg)
