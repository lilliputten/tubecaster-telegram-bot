from db import findUser


def checkValidUser(userId: int):
    user = findUser({'id': userId, 'isDeleted': False})
    return True if user is not None else False
