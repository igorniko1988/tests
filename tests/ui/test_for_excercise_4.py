from playwright.sync_api import Page, expect


def test_logged_in(authorized_user):
    data = authorized_user.evaluate("localStorage.getItem('token')")
    print(data)
    print(f'first {data}')

def test_fresh_page(page: Page):
    page.goto('/app')
    data = page.evaluate("localStorage.getItem('token')")
    print(f'second {data}')


def test_the_same_context(authorized_user):

    read_email = authorized_user.get_by_test_id("user-email").text_content()

    second_user = authorized_user.context.new_page()
    second_user.goto('/app')

    read_2nd_email = second_user.get_by_test_id("user-email").text_content()

    assert read_email == read_2nd_email

def test_two_users(create_user):
    first = create_user()
    second = create_user()

    first.goto('/app')


    second.goto('/http://localhost:8080/docs#/')

