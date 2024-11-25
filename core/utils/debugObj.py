from core.utils.variableAndKeyString import variableAndKeyString

space = ' - '


def debugObj(obj: dict[str, str | None], keys: list[str]):
    res = '\n'.join(
        list(
            filter(
                None,
                map(
                    lambda a: variableAndKeyString(obj, a),
                    keys,
                ),
            )
        )
    )
    res = space + res.strip().replace('\n', '\n' + space)
    return res
