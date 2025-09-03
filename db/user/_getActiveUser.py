from ._findUser import findUser


def getActiveUser(userId: int):
    return findUser({'id': userId, 'isDeleted': False})
