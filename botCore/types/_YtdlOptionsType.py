# -*- coding:utf-8 -*-

from typing import TypedDict, Optional


class YtdlOptionsType(TypedDict):
    cachedir: str
    extractor_args: Optional[str]
    outtmpl: Optional[str]
    _destFolder: Optional[str]
    _destFile: Optional[str]
    cookiefile: Optional[str]
    format: Optional[str]
    keepvideo: Optional[bool]
    verbose: Optional[bool]
    noplaylist: Optional[bool]
    #  debug_printtraffic: Optional[bool]
