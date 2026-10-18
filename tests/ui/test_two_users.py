def test_two_users_2(new_app):
    first = new_app()
    second = new_app()
    assert first.page.context != second.page.context