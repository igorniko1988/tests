import json

from framework.masking import hide_sensitive_fields


def format_body(content: bytes) -> str:
    if not content:
        return ""
    try:
        data = json.loads(content)
    except ValueError:
        return content.decode(errors="replace")
    masked = hide_sensitive_fields(data)
    return json.dumps(masked, indent=2, ensure_ascii=False)
