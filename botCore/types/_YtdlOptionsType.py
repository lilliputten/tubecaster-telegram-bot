# -*- coding:utf-8 -*-

from typing import Callable, Optional, TypedDict


class YtdlOptionsType(TypedDict, total=False):
    cachedir: str  # Required field
    extractor_args: Optional[dict[str, dict[str, list[str]]]]
    outtmpl: Optional[str]
    _destFolder: Optional[str]
    _destFile: Optional[str]
    cookiefile: Optional[str]
    format: Optional[str]
    keepvideo: Optional[bool]
    verbose: Optional[bool]
    noplaylist: Optional[bool]
    paths: Optional[dict[str, str]]
    extractor_retries: Optional[int]
    fragment_retries: Optional[int]
    retry_sleep_functions: Optional[dict[str, Callable[[int], float]]]
    #  listformats: Optional[bool]
    #  debug_printtraffic: Optional[bool]
