import re
from uuid import uuid4

from playwright.sync_api import Page, expect

from pages.issue_page import IssuePage
from pages.login_page import LoginPage


def test_create_issue(page: Page, credentials: tuple[str, str]) -> None:
    username, password = credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    issue_page = IssuePage(page)
    new_page = issue_page.open_create_issue()
    issue_page = IssuePage(new_page)

    issue_page.create_issue(
        "Тестовая задача Playwright", "Проверка автоматического создания задачи"
    )

    expect(issue_page.issue_summary).to_have_text("Тестовая задача Playwright")


def test_search_issue(page: Page, credentials: tuple[str, str]) -> None:
    username, password = credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    issue_page = IssuePage(page)
    issue_page.open_issues()
    expect(page).to_have_url(re.compile(r".*/issues/?"))
    expect(issue_page.search_input).to_be_visible()
    issue_page.search_issue("DEMO-16")
    expect(issue_page.get_issue_by_id("DEMO-16")).to_be_visible()


def test_change_issue_state(page: Page, credentials: tuple[str, str]) -> None:
    username, password = credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    issue_page = IssuePage(page)
    issue_page.open_issues()

    issue_link = issue_page.get_issue_by_id("DEMO-16")
    expect(issue_link).to_be_visible()

    issue_link.click()

    issue_page = IssuePage(page)

    expect(page).to_have_url(
        "http://localhost:8080/issue/DEMO-16/Monitor-your-progress"
    )
    issue_page.reset_state_to_do()
    expect(issue_page.state_button).to_have_attribute(
        "aria-label",
        "To do",
    )

    expect(issue_page.state_button).to_have_attribute(
        "aria-label",
        "To do",
    )

    issue_page.change_state()

    expect(issue_page.state_button).to_have_attribute(
        "aria-label",
        "In Progress",
    )


def test_add_comment(page: Page, credentials: tuple[str, str]) -> None:
    username, password = credentials

    page.goto("/")

    login_page = LoginPage(page)
    login_page.login(username, password)
    print("Авторизация выполнена")

    issue_page = IssuePage(page)
    issue_page.open_issues()

    issue_link = issue_page.get_issue_by_id("DEMO-16")
    expect(issue_link).to_be_visible()

    issue_link.click()

    expect(page).to_have_url(
        "http://localhost:8080/issue/DEMO-16/Monitor-your-progress"
    )

    comment_text = f"Playwright test comment {uuid4()}"

    issue_page.add_comment(comment_text)

    expect(issue_page.get_comment(comment_text)).to_be_visible()
