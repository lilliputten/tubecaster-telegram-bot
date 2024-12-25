import math


def getDesiredPiecesCount(fileSize: int, maxFileSize: int | None = None):
    if not maxFileSize or fileSize <= maxFileSize:
        return 1
    return math.ceil(fileSize / maxFileSize)
