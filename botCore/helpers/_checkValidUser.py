from db import findUser


def checkValidUser(userId: int):
    user = findUser(userId)
    return True if user else False
