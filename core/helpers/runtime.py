# -*- coding:utf-8 -*-

import os
import pathlib
import re
import traceback

_PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()


def getModulePath(deep: int | bool | None = None, traces: traceback.StackSummary | None = None):
    if not traces:
        limit = 2
        if type(deep) is int:   # isinstance(deep, int):
            limit = deep
        elif deep:
            limit = 3
        traces = traceback.extract_stack(None, limit)
    lastTrace = traces[0]
    modPath = pathlib.Path(lastTrace[0]).as_posix()
    if modPath.startswith(_PROJECT_PATH):
        modPath = modPath[len(_PROJECT_PATH) + 1 :]
    return modPath


def getFuncName(traces: traceback.StackSummary | None = None):
    if not traces:
        traces = traceback.extract_stack(None, 2)
    lastTrace = traces[0]
    funcName = lastTrace[2]
    return funcName


def getTrace(appendStr=None, traces: traceback.StackSummary | None = None):
    # NOTE: Required to pass extracted traceback
    if not traces:
        traces = traceback.extract_stack(None, 2)
    modPath = getModulePath(None, traces)
    modNameMatch = re.search(r'([^\\/]*).py$', modPath)
    modName = modNameMatch.group(1) if modNameMatch else modPath
    funcName = getFuncName(traces)
    strList = [
        '',
        #  __name__,
        modName,
        funcName if funcName != '<module>' else None,
        appendStr,
    ]
    filteredList = list(filter(None, strList))
    traceResult = '/'.join(filteredList)
    return traceResult
