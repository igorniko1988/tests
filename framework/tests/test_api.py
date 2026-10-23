


def test_me_endpoint_returns_data_with_valid_token(api, credentials):
    api.auth.register(**credentials)
    login = api.auth.login(**credentials)
    token = login.json()['access_token']
    api.client.set_token(token)

    r = api.auth.me()

    print(r.json())
    assert r.status_code == 200