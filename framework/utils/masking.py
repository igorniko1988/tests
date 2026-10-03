from typing import Any

HEADERS = ["authorization", "cookie"]
JSON_FIELDS = ["password", "access_token", "refresh_token"]


def hide_headers(request_headers: dict) -> dict:
    headers = {}
    for k, v in request_headers.items():
        if k.lower() in HEADERS:
            headers[k] = "****"
        else:
            headers[k] = v
    return headers


def hide_sensitive_fields(data: Any) -> Any:

    if isinstance(data, dict):
        sensitive_fields = {}
        for k, v in data.items():
            if k.lower() in JSON_FIELDS:
                sensitive_fields[k] = "****"
            else:
                sensitive_fields[k] = hide_sensitive_fields(v)
        return sensitive_fields
    if isinstance(data, list):
        list_of_sensitive_data = []
        for item in data:
            list_of_sensitive_data.append(hide_sensitive_fields(item))
        return list_of_sensitive_data
    return data
