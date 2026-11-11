from playwright.sync_api import Page, expect

from pages.issue_comments import IssueComments
from pages.issue_state import IssueState


class IssuePage:
    def __init__(self, page: Page):
        self.page = page
        self.issue_summary = page.locator('[data-test="ticket-summary"]')

        self.state = IssueState(page)
        self.comments = IssueComments(page)
        self.more_actions = page.locator('[data-test="issue-toolbar"]').get_by_role(
            "button",
            name="Show more",
            exact=True,
        )
        self.delete_menu_item = page.get_by_text("Delete issue", exact=True).locator(
            "xpath=../../.."
        )

        self.delete_dialog = page.get_by_role("dialog")
        self.confirm_delete_button = page.locator('[data-test="confirm-ok-button"]')

    def delete_issue(self) -> None:
        issue_url = self.page.url.split("?", maxsplit=1)[0]
        self.page.goto(issue_url)

        expect(self.issue_summary).to_be_visible()

        self.more_actions.click()
        self.delete_menu_item.click()

        expect(self.delete_dialog).to_be_visible()
        expect(self.confirm_delete_button).to_be_visible()
        expect(self.confirm_delete_button).to_be_enabled()

        self.confirm_delete_button.click()
        expect(self.delete_dialog).to_be_hidden()
