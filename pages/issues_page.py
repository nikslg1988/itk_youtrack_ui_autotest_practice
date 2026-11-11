from playwright.sync_api import Locator, Page

from pages.issue_create_page import IssueCreatePage


class IssuesPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder("Search for text or add a filter")
        self.create_menu = page.locator('[data-test="ring-dropdown create"] button')
        self.new_issue_link = page.get_by_role(
            "link",
            name="New issue",
            exact=True,
        )

    def open_issues(self) -> None:
        self.page.goto("/issues")

    def search_issue(self, issue_id: str) -> None:
        self.search_input.fill(issue_id)
        self.search_input.press("Enter")

    def get_issue_by_id(self, issue_id: str) -> Locator:
        return self.page.get_by_role(
            "link",
            name=issue_id,
            exact=True,
        )

    def open_create_issue(self) -> IssueCreatePage:
        self.create_menu.click()

        with self.page.expect_popup() as popup_info:
            self.new_issue_link.click()

        return IssueCreatePage(popup_info.value)
