from core.helpers.strings import ansiStyle


def errorTitleStyle(s: str):
    return ansiStyle(s, 'underline', 'bold', 'red')


def warningITitlenfo(s: str):
    return ansiStyle(s, 'underline', 'bold', 'yellow')


def errorStyle(s: str):
    return ansiStyle(s, 'red')


def warningStyle(s: str):
    return ansiStyle(s, 'yellow')


def titleStyle(s: str):
    return ansiStyle(s, 'underline', 'bold')


def primaryStyle(s: str):
    return ansiStyle(s, 'underline', 'bold', 'green')


def secondaryStyle(s: str):
    return ansiStyle(s, 'cyan')


def tretiaryStyle(s: str):
    return ansiStyle(s, 'blue')
