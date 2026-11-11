from playwright.sync_api import Page


class IssueState:
    def __init__(self, page: Page):
        self.state_field = page.locator('[aria-label="State"]')
        self.state_button = self.state_field.get_by_role("combobox")

        self.state_options = {
            "To do": page.locator('[data-test="ring-list-item-label"][title="To do"]'),
            "In Progress": page.locator(
                '[data-test="ring-list-item-label"][title="In Progress"]'
            ),
        }

    def set_state(self, state: str) -> None:
        if state not in self.state_options:
            raise ValueError(f"Неизвестный статус: {state}")

        self.state_button.click()
        self.state_options[state].click()
