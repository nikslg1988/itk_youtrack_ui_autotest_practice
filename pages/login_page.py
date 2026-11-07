from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = self.page.locator('[name="username"]')
        self.password = self.page.locator('[name="password"]')
        self.login_button = self.page.locator('[data-test="login-button"]')
        self.error_message = self.page.locator('[data-test="error-message"]')

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
