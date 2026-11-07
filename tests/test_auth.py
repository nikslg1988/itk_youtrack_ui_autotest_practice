import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_successful_login(page: Page, credentials: tuple[str, str]) -> None:
    username, password = credentials

    page.goto("/")
    login_page = LoginPage(page)
    login_page.login(username, password)

    expect(page.locator('[data-test="ring-dropdown ring-profile"]')).to_be_visible()


@pytest.mark.parametrize(
    "invalid_credentials",
    ["wrong_username", "wrong_password"],
    indirect=True,
)
def test_failed_login(
    page: Page,
    invalid_credentials: tuple[str, str],
) -> None:
    username, password = invalid_credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
