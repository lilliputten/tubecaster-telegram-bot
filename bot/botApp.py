# -*- coding:utf-8 -*-

import traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.appConfig import appConfig
from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger

# @see https://python-telegram-bot.org/
# @see https://docs.python-telegram-bot.org/

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise Exception('No telegram token defined')

#  changed = appConfig.get('changed')

logger = getLogger('bot/botApp')

logger.info('Token: %s' % TELEGRAM_TOKEN)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sample bot command
    """
    timeStamp = getTimeStamp(True)
    message = update.message
    effective_user = update.effective_user
    userName = effective_user.first_name if effective_user else 'Noname'
    logger.info('test message %s: test %s' % (timeStamp, userName))
    if message:
        await message.reply_text(f'Test {userName}: {timeStamp}')


# Start bot...

botApp = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

botApp.add_handler(CommandHandler('test', test))


def startBot():
    try:
        timeStamp = getTimeStamp(True)
        logger.info('Starting bot, %s' % timeStamp)
        botApp.run_polling()
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        logger.error('Caught error %s (re-raising): %s', sError, sTraceback)


# Module exports...
__all__ = [
    'botApp',
    'startBot',
]
