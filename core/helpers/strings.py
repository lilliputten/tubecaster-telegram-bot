def truncStr(str: str, maxLen: int):
    if len(str) >= maxLen - 3:
        str = str[: maxLen - 3] + '...'
    return str
