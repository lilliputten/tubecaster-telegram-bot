commandsInfo = {
    'start': 'Gives information about the bot.',
    'help': 'Gives information about all of the available commands.',
    'info URL': 'Show information about the YouTube video.',
    'cast URL': 'Convert YouTube video to audio for listening.',
}

# Provide commands list in the format of `{command} - {explanation}`
_infoStr = '\n'.join(['%s - %s' % (k.split()[0], commandsInfo[k]) for k in commandsInfo])
print('\nHere are the bot commands list to provide to the BotFather:\n\n' + _infoStr + '\n')

hiddenCommands = [
    'castTest',
    'test',
]

__all__ = [
    'commandsInfo',
    'hiddenCommands',
]
