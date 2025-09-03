# -*- coding:utf-8 -*-

from core.logger import getDebugLogger, tretiaryStyle


_logger = getDebugLogger()


# NOTE: Use 'Edit commands' menu in the bot managememnt panel to update menu entries
commandsInfo = {
    'cast URL': 'Convert YouTube video to audio for listening.',
    'info URL': 'Show information about the YouTube video.',
    'stats': 'Display your statistics (request and failure counts, overall downloaded audio files size, total and monthly).',
    'status': 'Show your status (membership, registration, etc).',
    'plans': 'Show details on available usage plans (guest, free, paid).',
    'become_user': 'Request a registration to gain access to the free bot functionality.',
    'get_full_access': 'Obtain a full (paid) access mode. See /plans for detailed information about available plans.',
    'remove_account': 'Remove your user account and all the data completely.',
    'restore_account': 'Restore removed account, if less than a month has passed since the deletion.',
    'start': 'Gives generic information about the bot.',
    'help': 'Gives information about all of the available commands.',
}

hiddenCommands = [
    'cast_test',
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
