import json
from datetime import timedelta

import httpx
from pytest import fixture

from framework.http.http_logging import format_body, format_headers, format_request, format_response


@fixture
def login_request():
    return httpx.Request(
        "POST",
        "http://test/auth/login",
        json={"email": "a@b.com", "password": "123"},
        headers={"Authorization": "Bearer abc"},
    )


@fixture
def login_response(login_request):
    response = httpx.Response(
        200, json={"access_token": "xyz", "token_type": "bearer"}, request=login_request
    )

    response.elapsed = timedelta(milliseconds=34)
    return response


def test_headers_authorization_masked(login_request):
    result = format_headers(login_request.headers)
    assert "authorization: ****" in result
    assert "Bearer abc" not in result


def test_request_starts_with_method_and_url(login_request):
    result = format_request(login_request)
    assert result.startswith("POST http://test/auth/login")


def test_request_hides_token(login_request):
    result = format_request(login_request)
    assert "Bearer abc" not in result


def test_request_hides_password(login_request):
    result = format_request(login_request)
    assert '"123"' not in result
    assert "a@b.com" in result


def test_response_starts_with_status_and_time(login_response):
    result = format_response(login_response)
    assert result.startswith("200 OK (0.034 s)")


def test_response_hides_access_token(login_response):
    result = format_response(login_response)
    assert "xyz" not in result
    assert "bearer" in result


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
