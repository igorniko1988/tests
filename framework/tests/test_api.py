def test_me_endpoint_returns_data_with_valid_token(auth_api):
    r = auth_api.get('/me')

    print(r.json())
    assert r.status_code == 200