from playwright.sync_api import Page


class IssueCreatePage:
    def __init__(self, page: Page):
        self.page = page
        self.summary = page.locator('[data-test="summary"]')
        self.description = page.locator('[data-test="wysiwyg-editor-content"]')
        self.create_button = page.locator('[data-test="submit-button"]')
        self.issue_summary = page.locator('[data-test="ticket-summary"]')

    def create_issue(self, summary: str, description: str) -> None:
        self.summary.fill(summary)
        self.description.fill(description)
        self.create_button.click()
