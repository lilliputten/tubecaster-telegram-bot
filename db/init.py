import sys
from typing import Any, Optional
from flask.ctx import _AppCtxGlobals
from prisma import Prisma, register, get_client

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:
    from flask import Flask, g
    if 'DB' in g:
        db = g.get('DB')
    pass


# def get_db() -> Prisma:
#     try:
#         return g.db
#     except AttributeError:
#         g.db = db = Prisma()
#         db.connect()
#         return db

_db: Optional[Prisma] = None

# TGlobalCtx = Optional[dict[str, Any]]
TGlobalCtx = _AppCtxGlobals

def openDb(g: Optional[TGlobalCtx]) -> Prisma:
    global _db
    # gs = globals()
    if not _db:
        if g is not None and 'DB' in g:
            # Try to get db from global object...
            _db = g.DB
        _db = Prisma()
    if g is not None:
        # TODO: Check for _AppCtxGlobals
        g.DB = _db
    if not _db.is_connected():
        _db.connect()
    return _db



def closeDb(_exc: Optional[Exception] = None) -> None:  # noqa: ARG001
    if _exc:
        print('closeDb exc:', repr(_exc))
    client = get_client()
    if client.is_connected():
        client.disconnect()

# register(openDb)
# flaskApp.teardown_appcontext(closeDb)

# def registerDbForFlaskApp(flaskApp: )
