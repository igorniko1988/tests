import json

import httpx

from framework.utils.masking import hide_headers, hide_sensitive_fields


def format_body(content: bytes) -> str:
    if not content:
        return ""
    try:
        data = json.loads(content)
    except ValueError:
        return content.decode(errors="replace")
    masked = hide_sensitive_fields(data)
    return json.dumps(masked, indent=2, ensure_ascii=False)


def format_headers(headers: httpx.Headers) -> str:
    masked = hide_headers(dict(headers))
    return "\n".join(f"{k}: {v}" for k, v in masked.items())


def format_request(request: httpx.Request) -> str:
    first_line = f"{request.method} {request.url}"
    headers = format_headers(request.headers)
    body = format_body(request.content)
    return f"{first_line}\n\n{headers}\n\n{body}"


def format_response(response: httpx.Response) -> str:
    seconds = response.elapsed.total_seconds()
    first_line = f"{response.status_code} {response.reason_phrase} ({seconds:.3f} s)"
    headers = format_headers(response.headers)
    body = format_body(response.content)
    return f"{first_line}\n\n{headers}\n\n{body}"
