import re

from playwright.sync_api import Page, expect


def test_smoke(page: Page) -> None:
    page.goto("/")
    expect(page).to_have_title(re.compile("YouTrack"))
