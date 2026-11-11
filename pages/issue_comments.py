from playwright.sync_api import Locator, Page


class IssueComments:
    def __init__(self, page: Page):
        self.page = page
        self.comment_editor = page.locator(
            '[data-test="wysiwyg-editor-content"][contenteditable="true"]'
        )
        self.comment_submit = page.locator('[data-test="post-comment"]')
        self.comment_content = page.locator('[data-test="comment-content"]')

    def add_comment(self, text: str) -> None:
        self.comment_editor.fill(text)
        self.comment_submit.click()

    def get_comment(self, text: str) -> Locator:
        return self.comment_content.get_by_text(text, exact=True)
