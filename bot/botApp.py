# -*- coding:utf-8 -*-

from core.appConfig import appConfig
from core.logger import getLogger

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# @see https://python-telegram-bot.org/
# @see https://docs.python-telegram-bot.org/

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise Exception('No telegram token defined')

changed = """
@changed 2024.11.23, 22:53
""".strip().replace(
    '@changed ', ''
)

logger = getLogger('bot/botApp')

logger.info('Start: %s' % changed)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    effective_user = update.effective_user
    userName = effective_user.first_name if effective_user else 'Anonymous'
    logger.info('%s: test %s' % (changed, userName))
    if message:
        await message.reply_text(f'Test {userName}: {changed}')


# Start bot...

botApp = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

botApp.add_handler(CommandHandler('test', test))

#  botApp.run_polling()  # Do it in the root app


# Module exports...
__all__ = [
    'botApp',
]
