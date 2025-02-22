from db import findUser


def checkValidUser(userId: int):
    user = findUser(userId)
    return True if user is not None else False
