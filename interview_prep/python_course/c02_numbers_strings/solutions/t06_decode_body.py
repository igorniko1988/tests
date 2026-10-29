import codecs


def charset_from(content_type: str | None) -> str:
    if not content_type:
        return "utf-8"
    for part in content_type.split(";")[1:]:  # первая часть — сам тип, text/plain
        key, _, value = part.partition("=")
        if key.strip().lower() == "charset":
            return value.strip().strip('"') or "utf-8"
    return "utf-8"


def decode_body(data: bytes, content_type: str | None = None) -> str:
    encoding = charset_from(content_type)
    try:
        codecs.lookup(encoding)
    except LookupError:
        encoding = "utf-8"
    return data.decode(encoding, errors="replace")
