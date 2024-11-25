def variableAndKeyString(obj: dict[str, str | bool | int | None], key: str):
    """
    Debug helper: create object variable line, if exists.
    """
    val = obj.get(key)
    if not val:
        return None
    return key + ': ' + str(val)


__all__ = [
    'variableAndKeyString',
]
