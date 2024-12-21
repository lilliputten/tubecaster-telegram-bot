
from core.helpers.strings import ansiStyle



def errorInfo(s: str):
    return ansiStyle(s, 'red')

def warningInfo(s: str):
    return ansiStyle(s, 'yellow')

def titleInfo(s: str):
    return ansiStyle(s, 'underline', 'bold')

def primaryInfo(s: str):
    return ansiStyle(s, 'underline', 'bold', 'green')

def secondaryInfo(s: str):
    return ansiStyle(s, 'cyan')

def tretiaryInfo(s: str):
    return ansiStyle(s, 'blue')
