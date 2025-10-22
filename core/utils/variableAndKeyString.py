def variableAndKeyString(obj: dict[str, str | bool | int | None], key: str, limit: int | None = None):
    """
    Debug helper: create object variable line, if exists.
    """
    val = obj.get(key)
    if not val:
        return None
    str_val = str(val)
    if limit and len(str_val) > limit:
        str_val = str_val[:limit] + '...'
    return key + ': ' + str_val


__all__ = [
    'variableAndKeyString',
]
