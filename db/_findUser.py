from prisma.models import User


def findUser(id: int):
    userClient = User.prisma()
    try:
        user = userClient.find_unique(
            where={
                'id': id,
            },
        )
        return user
    finally:
        pass
