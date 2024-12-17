# -*- coding:utf-8 -*-

import traceback
import re

def getTrace(appendStr=None):
    # NOTE: Required to pass extracted traceback
    traces = traceback.extract_stack(None, 2)
    lastTrace = traces[0]
    modPath = lastTrace[0]
    modNameMatch = re.search(r'([^\\/]*).py$', modPath)
    modName = modNameMatch.group(1) if modNameMatch else modPath
    funcName = lastTrace[2]
    strList = [
        '',
        #  __name__,
        modName,
        funcName,
        appendStr,
    ]
    filteredList = list(filter(None, strList))
    traceResult = '/'.join(filteredList)
    return traceResult

