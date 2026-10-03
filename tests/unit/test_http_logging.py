import json

from framework.http_logging import format_body


def test_json_body_password_is_masked():
    data = b'{"email":"a@b.com","password":"123"}'

    result = format_body(data)

    assert json.loads(result) == {"email": "a@b.com", "password": "****"}


def test_empty_body_returns_empty_string():

    result = format_body(b"")

    assert result == ""


def test_not_json_body_returned_as_text():

    data = b"not a json"

    result = format_body(data)

    assert result == "not a json"


def test_binary_body_does_not_fail():

    data = b"\xff\xfe"

    result = format_body(data)

    assert isinstance(result, str)


def test_cyrillic_is_readable():

    data = '{"name":"Игорь"}'.encode()

    result = format_body(data)

    assert "Игорь" in result
