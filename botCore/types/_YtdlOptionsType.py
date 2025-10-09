# -*- coding:utf-8 -*-

from typing import Optional, TypedDict


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
    paths: Optional[dict[str, str]]
    #  listformats: Optional[bool]
    #  debug_printtraffic: Optional[bool]
