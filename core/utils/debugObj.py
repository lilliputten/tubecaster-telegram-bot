from core.utils.variableAndKeyString import variableAndKeyString


def debugObj(obj: dict[str, str | None], keys: list[str]):
    return '\n'.join(
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
