def flatten(data: dict, sep: str = ".") -> dict:
    result = {}

    def walk(node: dict, prefix: str) -> None:
        for key, value in node.items():
            path = f"{prefix}{sep}{key}" if prefix else str(key)
            if isinstance(value, dict) and value:
                walk(value, path)
            else:
                result[path] = value

    walk(data, "")
    return result
