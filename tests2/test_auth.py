def test_getting_token(authorized_api):
    r = authorized_api.me()

    print(r.json())