import re
from uuid import uuid4

from playwright.sync_api import Page, expect

from pages.issues_page import IssuesPage


def test_create_issue(created_issue) -> None:
    issue_page, summary, description = created_issue

    expect(issue_page.issue_summary).to_have_text(summary)

    expect(issue_page.page.get_by_text(description, exact=True)).to_be_visible()


def test_search_issue(authenticated_page: Page) -> None:
    issues_page = IssuesPage(authenticated_page)
    issues_page.open_issues()

    expect(authenticated_page).to_have_url(re.compile(r".*/issues/?"))
    expect(issues_page.search_input).to_be_visible()

    issues_page.search_issue("DEMO-16")

    expect(issues_page.get_issue_by_id("DEMO-16")).to_be_visible()


def test_change_issue_state(created_issue) -> None:
    issue_page, summary, description = created_issue

    expect(issue_page.state.state_button).to_have_attribute("aria-label", "To do")

    issue_page.state.set_state("In Progress")

    expect(issue_page.state.state_button).to_have_attribute("aria-label", "In Progress")


def test_add_comment(created_issue) -> None:
    issue_page, _, _ = created_issue

    comment_text = f"Playwright test comment {uuid4()}"

    issue_page.comments.add_comment(comment_text)

    expect(issue_page.comments.get_comment(comment_text)).to_be_visible()
