# -*- coding:utf-8 -*-

import traceback
import re
import os
import pathlib

_PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()


def getModPath(traces: traceback.StackSummary | None = None):
    # NOTE: Required to pass extracted traceback
    if not traces:
        traces = traceback.extract_stack(None, 2)
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
    modPath = getModPath(traces)
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
