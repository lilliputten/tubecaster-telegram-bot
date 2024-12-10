import math


def getDesiredPiecesCount(fileSize: int, maxFileSize: int):
    if fileSize <= maxFileSize:
        return 1
    return math.ceil(fileSize / maxFileSize)
