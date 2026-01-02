"""Tests for the Playwright to Robot Framework converter."""

from robotframework_browser_recorder.converter.playwright_to_robot import (
    PlaywrightToRobotConverter,
)


class TestPlaywrightToRobotConverter:
    """Test cases for PlaywrightToRobotConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = PlaywrightToRobotConverter()

    def test_convert_goto(self):
        """Test converting page.goto() action."""
        playwright_code = 'page.goto("https://example.com")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "goto"
        assert actions[0]["url"] == "https://example.com"

    def test_convert_click(self):
        """Test converting click action."""
        playwright_code = 'page.click("#submit-button")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "click"
        assert actions[0]["selector"] == "#submit-button"

    def test_convert_fill(self):
        """Test converting fill action."""
        playwright_code = 'page.fill("#username", "testuser")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "fill"
        assert actions[0]["selector"] == "#username"
        assert actions[0]["value"] == "testuser"

    def test_convert_fill_with_locator(self):
        """Test converting fill action with locator chain."""
        playwright_code = 'page.locator("#username").fill("testuser")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "fill"
        assert actions[0]["selector"] == "#username"
        assert actions[0]["value"] == "testuser"

    def test_convert_select_option_with_locator(self):
        """Test converting select_option with locator chain."""
        playwright_code = 'page.locator("#country").select_option("USA")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "select_option"
        assert actions[0]["selector"] == "#country"
        assert actions[0]["value"] == "USA"

    def test_convert_check(self):
        """Test converting check action."""
        playwright_code = 'page.check("#agree-checkbox")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "check"
        assert actions[0]["selector"] == "#agree-checkbox"

    def test_convert_multiple_actions(self):
        """Test converting multiple actions."""
        playwright_code = """
page.goto("https://example.com/login")
page.fill("#username", "user1")
page.fill("#password", "pass123")
page.click("#submit")
"""
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 4
        assert actions[0]["type"] == "goto"
        assert actions[1]["type"] == "fill"
        assert actions[2]["type"] == "fill"
        assert actions[3]["type"] == "click"

    def test_generate_robot_test(self):
        """Test generating complete Robot Framework test."""
        playwright_code = """
page.goto("https://example.com")
page.click("text=Login")
"""
        robot_test = self.converter.convert(
            playwright_code=playwright_code,
            test_name="Example Test",
            browser="chromium",
            headless=False,
        )

        assert "*** Settings ***" in robot_test
        assert "Library    Browser" in robot_test
        assert "*** Test Cases ***" in robot_test
        assert "Example Test" in robot_test
        assert "New Browser    chromium    headless=False" in robot_test
        assert "New Page    https://example.com" in robot_test
        assert "Click    text=Login" in robot_test

    def test_extract_selector_with_locator(self):
        """Test extracting selector from locator method."""
        line = 'page.locator("#username").fill("test")'
        selector = self.converter._extract_selector(line)
        assert selector == "#username"

    def test_extract_selector_with_get_by_text(self):
        """Test extracting selector from get_by_text method."""
        line = 'page.get_by_text("Login").click()'
        selector = self.converter._extract_selector(line)
        assert selector == "Login"

    def test_convert_hover(self):
        """Test converting hover action."""
        playwright_code = 'page.hover("#menu-item")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "hover"
        assert actions[0]["selector"] == "#menu-item"

    def test_convert_double_click(self):
        """Test converting double-click action."""
        playwright_code = 'page.dblclick("#file-item")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "dblclick"
        assert actions[0]["selector"] == "#file-item"

    def test_ignore_comments_and_imports(self):
        """Test that comments and imports are ignored."""
        playwright_code = """
# This is a comment
import playwright
from playwright.sync_api import sync_playwright

page.goto("https://example.com")
"""
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "goto"

    def test_convert_expect_visible(self):
        """Test converting expect().to_be_visible() assertion."""
        playwright_code = 'expect(page.locator("#message")).to_be_visible()'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_visible"
        assert actions[0]["selector"] == "#message"

    def test_convert_expect_text(self):
        """Test converting expect().to_have_text() assertion."""
        playwright_code = 'expect(page.locator("#title")).to_have_text("Welcome")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_text"
        assert actions[0]["selector"] == "#title"
        assert actions[0]["text"] == "Welcome"

    def test_convert_expect_value(self):
        """Test converting expect().to_have_value() assertion."""
        playwright_code = 'expect(page.locator("#email")).to_have_value("test@example.com")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_value"
        assert actions[0]["selector"] == "#email"
        assert actions[0]["value"] == "test@example.com"

    def test_convert_expect_checked(self):
        """Test converting expect().to_be_checked() assertion."""
        playwright_code = 'expect(page.locator("#agree")).to_be_checked()'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_checked"
        assert actions[0]["selector"] == "#agree"

    def test_convert_set_input_files(self):
        """Test converting set_input_files action with locator chain."""
        playwright_code = 'page.locator("#upload").set_input_files("document.pdf")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "set_input_files"
        assert actions[0]["selector"] == "#upload"
        assert actions[0]["file_path"] == "document.pdf"

    def test_convert_expect_url(self):
        """Test converting expect(page).to_have_url() assertion."""
        playwright_code = 'expect(page).to_have_url("https://example.com/dashboard")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_url"
        assert actions[0]["url"] == "https://example.com/dashboard"

    def test_convert_expect_title(self):
        """Test converting expect(page).to_have_title() assertion."""
        playwright_code = 'expect(page).to_have_title("Dashboard")'
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 1
        assert actions[0]["type"] == "expect_title"
        assert actions[0]["title"] == "Dashboard"

    def test_convert_with_assertions(self):
        """Test converting a complete flow with assertions."""
        playwright_code = """
page.goto("https://example.com/login")
page.fill("#username", "user1")
page.fill("#password", "pass123")
page.click("#submit")
expect(page).to_have_url("https://example.com/dashboard")
expect(page.locator("#welcome-message")).to_be_visible()
expect(page.locator("#welcome-message")).to_have_text("Welcome, user1!")
"""
        actions = self.converter._parse_playwright_code(playwright_code)
        assert len(actions) == 7
        assert actions[0]["type"] == "goto"
        assert actions[4]["type"] == "expect_url"
        assert actions[5]["type"] == "expect_visible"
        assert actions[6]["type"] == "expect_text"
