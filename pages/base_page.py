"""Base page class for all page objects."""
from playwright.sync_api import Page, expect


class BasePage:
    """Base page class containing common functionality for all pages."""

    def __init__(self, page: Page):
        """Initialize base page with Playwright page object.
        
        Args:
            page: Playwright page object
        """
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a specific URL.
        
        Args:
            url: The URL to navigate to
        """
        self.page.goto(url)

    def fill_input(self, selector: str, value: str):
        """Fill an input field with a value.
        
        Args:
            selector: CSS selector or other selector for the input field
            value: The value to fill in
        """
        self.page.fill(selector, value)

    def click_element(self, selector: str):
        """Click an element.
        
        Args:
            selector: CSS selector or other selector for the element
        """
        self.page.click(selector)

    def upload_file(self, selector: str, file_path: str):
        """Upload a file to a file input.
        
        Args:
            selector: CSS selector for the file input
            file_path: Path to the file to upload
        """
        self.page.set_input_files(selector, file_path)

    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Wait for an element to be visible.
        
        Args:
            selector: CSS selector for the element
            timeout: Maximum time to wait in milliseconds
        """
        self.page.wait_for_selector(selector, timeout=timeout)
