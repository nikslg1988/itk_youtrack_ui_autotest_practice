from playwright.sync_api import Page


class IssuePage:
    def __init__(self, page: Page):
        self.page = page
        self.summary = self.page.locator('[data-test="summary"]')
        self.description = self.page.locator('[data-test="wysiwyg-editor-content"]')
        self.create_button = self.page.locator('[data-test="submit-button"]')
        self.create_menu = self.page.locator(
            '[data-test="ring-dropdown create"] button'
        )
        self.new_issue_link = self.page.get_by_role("link", name="New issue")
        self.issue_summary = self.page.locator('[data-test="ticket-summary"]')
        self.search_input = self.page.get_by_placeholder(
            "Search for text or add a filter"
        )
        self.search_button = self.page.locator('[data-test="search-button"]')
        self.issues_link = self.page.locator('[data-test="ring-link issues-button"]')
        self.state_field = self.page.locator('[aria-label="State"]')
        self.state_button = self.state_field.get_by_role("combobox")
        self.state_option_in_progress = self.page.locator(
            '[data-test="ring-list-item-label"][title="In Progress"]'
        )
        self.state_option_to_do = self.page.locator(
            '[data-test="ring-list-item-label"][title="To do"]'
        )
        self.comment_editor = self.page.locator(
            '[data-test="wysiwyg-editor-content"][contenteditable="true"]'
        )
        self.comment_submit = self.page.locator('[data-test="post-comment"]')
        self.comment_content = self.page.locator('[data-test="comment-content"]')

    def open_create_issue(self) -> Page:
        self.create_menu.click()
        with self.page.expect_popup() as popup_info:
            self.new_issue_link.click()

        new_page = popup_info.value
        return new_page

    def create_issue(self, summary: str, description: str) -> None:
        self.summary.fill(summary)
        self.description.fill(description)
        self.create_button.click()

    def search_issue(self, issue_id: str) -> None:
        self.search_input.fill(issue_id)
        self.search_input.press("Enter")

    def open_issues(self) -> None:
        self.page.goto("/issues")

    def get_issue_by_id(self, issue_id: str):
        return self.page.get_by_role("link", name=issue_id, exact=True)

    def change_state(self):
        self.state_button.click()
        self.state_option_in_progress.click()

    def reset_state_to_do(self) -> None:
        self.state_button.click()
        self.state_option_to_do.click()

    def add_comment(self, text: str) -> None:
        self.comment_editor.fill(text)
        self.comment_submit.click()

    def get_comment(self, text: str):
        return self.comment_content.filter(has_text=text)
