import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

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
        page = item.funcargs["page"]
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
