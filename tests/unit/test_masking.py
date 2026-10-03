from framework.utils.masking import hide_headers, hide_sensitive_fields

MASK = "****"


def test_authorization_header_is_masked():
    data = {"Authorization": "Bearer abc", "Content-Type": "application/json"}

    result = hide_headers(data)

    assert result == {"Authorization": MASK, "Content-Type": "application/json"}


def test_header_name_case_insensitive():
    data = {"authorization": "Bearer abc"}

    result = hide_headers(data)

    assert result["authorization"] == MASK


def test_password_is_masked():
    data = {"email": "a@b.com", "password": "123"}

    result = hide_sensitive_fields(data)

    assert result == {"email": "a@b.com", "password": MASK}


def test_nested_field_is_masked():
    data = {"user": {"password": "123"}}

    result = hide_sensitive_fields(data)

    assert result == {"user": {"password": MASK}}


def test_test_fields_inside_list_are_masked():
    data = {"items": [{"access_token": "a"}, {"access_token": "b"}]}

    result = hide_sensitive_fields(data)

    assert result == {"items": [{"access_token": MASK}, {"access_token": MASK}]}


def test_non_container_returned_as_is():
    data = "text", 42, None

    result = hide_sensitive_fields(data)

    assert result == data
