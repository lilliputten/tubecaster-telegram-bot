import datetime
import traceback
from datetime import date

from prisma.models import Command
from prisma.types import CommandWhereInput, DateTimeFilter

from core.helpers.errors import errorToString

validHours = 1


def deleteOutdatedCommands(outdatedDate: date | None = None):
    commandClient = Command.prisma()
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        if outdatedDate is None:
            outdatedDate = now - datetime.timedelta(hours=validHours)
        # commands = commandClient.find_many(
        #     where={
        #         'createdAt': { 'lt': outdatedDate },
        #     },
        # )
        # command = commands[0] if len(commands) > 0 else None
        # print(f'Found {len(commands)} commands: {commands}')
        # if command:
        #     print('command.id', command.id)
        #     print('              now:', now)
        #     print('         outdatedDate:', outdatedDate)
        #     print('command.createdAt:', command.createdAt)
        #     print('command.updatedAt:', command.updatedAt)
        createdAtFilter: DateTimeFilter = {'lt': outdatedDate}  # type: ignore
        where: CommandWhereInput = {
            'createdAt': createdAtFilter,
        }
        return commandClient.delete_many(
            where=where,
        )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
    finally:
        pass
