# -*- coding:utf-8 -*-

from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.appConfig import appConfig
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
    timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    message = update.message
    effective_user = update.effective_user
    userName = effective_user.first_name if effective_user else 'Noname'
    logger.info('test message %s: test %s' % (timeStr, userName))
    if message:
        await message.reply_text(f'Test {userName}: {timeStr}')


# Start bot...

botApp = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

botApp.add_handler(CommandHandler('test', test))


# Module exports...
__all__ = [
    'botApp',
]
