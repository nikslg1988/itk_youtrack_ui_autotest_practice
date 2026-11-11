import os
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from pages.issue_page import IssuePage
from pages.issues_page import IssuesPage
from pages.login_page import LoginPage

SCREENSHOTS_DIR = Path("artifacts/screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def credentials() -> tuple[str, str]:
    load_dotenv()
    username = os.getenv("YOUTRACK_USERNAME")
    password = os.getenv("YOUTRACK_PASSWORD")
    if username is None or password is None:
        raise ValueError("Не заданы YOUTRACK_USERNAME или YOUTRACK_PASSWORD")
    return (username, password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page is not None:
            screenshot_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = SCREENSHOTS_DIR / f"{screenshot_name}.png"

            page.screenshot(
                path=str(screenshot_path),
                full_page=True,
            )


@pytest.fixture
def invalid_credentials(request, credentials):
    username, password = credentials

    if request.param == "wrong_username":
        return ("wrong_user", password)

    if request.param == "wrong_password":
        return (username, "another_wrong_password")

    raise ValueError(f"Неизвестный сценарий: {request.param}")


@pytest.fixture
def authenticated_page(
    page: Page,
    credentials: tuple[str, str],
) -> Page:
    username, password = credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    expect(page.locator('[data-test="ring-dropdown ring-profile"]')).to_be_visible()

    return page


@pytest.fixture
def created_issue(
    authenticated_page: Page,
) -> Iterator[tuple[IssuePage, str, str]]:

    issues_page = IssuesPage(authenticated_page)
    issue_create_page = issues_page.open_create_issue()

    summary = f"Playwright test issue {uuid4()}"
    description = f"Automated test description {uuid4()}"

    issue_create_page.create_issue(summary, description)

    issue_page = IssuePage(issue_create_page.page)

    try:
        expect(issue_page.issue_summary).to_have_text(summary)

        yield issue_page, summary, description

    finally:
        issue_page.delete_issue()
