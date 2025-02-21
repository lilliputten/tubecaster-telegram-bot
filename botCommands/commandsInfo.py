# -*- coding:utf-8 -*-

from core.logger import getDebugLogger, tretiaryStyle


_logger = getDebugLogger()


commandsInfo = {
    'cast URL': 'Convert YouTube video to audio for listening.',
    'info URL': 'Show information about the YouTube video.',
    'register': 'Request access reqistration.',
    'start': 'Gives information about the bot.',
    'help': 'Gives information about all of the available commands.',
}

hiddenCommands = [
    'castTest',
    'test',
]


def showInfo():
    # Provide commands list in the format of `{command} - {explanation}`
    infoStr = '\n'.join(['%s - %s' % (k.split()[0], commandsInfo[k]) for k in commandsInfo])
    infoItems = [
        '',
        'Here are the bot commands list to provide (via copy/paste) to the BotFather:',
        infoStr,
        #  '',
    ]
    infoContent = tretiaryStyle('\n\n'.join(infoItems)) + '\n'
    _logger.info(infoContent)


showInfo()


__all__ = [
    'commandsInfo',
    'hiddenCommands',
]
