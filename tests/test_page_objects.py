"""Unit tests for page object model structure."""
import pytest
import os
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.greenhouse_page import GreenhousePage


# Path to test resume
TEST_RESUME_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_resume.pdf")


def test_base_page_initialization(page: Page):
    """Test that BasePage can be initialized with a Playwright page.
    
    Args:
        page: Playwright page fixture
    """
    base_page = BasePage(page)
    assert base_page.page == page


def test_greenhouse_page_initialization(page: Page):
    """Test that GreenhousePage can be initialized with a Playwright page.
    
    Args:
        page: Playwright page fixture
    """
    greenhouse_page = GreenhousePage(page)
    assert greenhouse_page.page == page
    assert isinstance(greenhouse_page, BasePage)


def test_greenhouse_page_has_required_selectors():
    """Test that GreenhousePage has all required selectors defined."""
    selectors = [
        GreenhousePage.FIRST_NAME_INPUT,
        GreenhousePage.LAST_NAME_INPUT,
        GreenhousePage.EMAIL_INPUT,
        GreenhousePage.PHONE_INPUT,
        GreenhousePage.RESUME_INPUT,
        GreenhousePage.COUNTRY_INPUT,
    ]
    
    for selector in selectors:
        assert selector is not None
        assert isinstance(selector, str)
        assert len(selector) > 0


def test_greenhouse_page_has_required_methods():
    """Test that GreenhousePage has all required methods."""
    methods = [
        'open_job_application',
        'fill_first_name',
        'fill_last_name',
        'fill_email',
        'fill_phone',
        'fill_country',
        'attach_resume',
        'fill_application',
        'verify_first_name_field',
        'verify_last_name_field',
        'verify_email_field',
        'verify_phone_field',
        'verify_resume_field',
        'get_first_name_value',
        'get_last_name_value',
        'get_email_value',
        'get_phone_value',
        'verify_file_attached',
    ]
    
    for method in methods:
        assert hasattr(GreenhousePage, method)
        assert callable(getattr(GreenhousePage, method))


def test_test_resume_exists():
    """Test that the test resume PDF file exists."""
    assert os.path.exists(TEST_RESUME_PATH), f"Test resume not found at {TEST_RESUME_PATH}"
    assert os.path.isfile(TEST_RESUME_PATH), f"Test resume path is not a file: {TEST_RESUME_PATH}"
    
    # Verify it's a PDF file (basic check)
    with open(TEST_RESUME_PATH, 'rb') as f:
        header = f.read(4)
        assert header == b'%PDF', "Test resume is not a valid PDF file"


def test_greenhouse_page_methods_with_mock_html(page: Page):
    """Test GreenhousePage methods with a mock HTML form.
    
    Args:
        page: Playwright page fixture
    """
    # Create a mock HTML page with a Greenhouse-like form
    mock_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Mock Greenhouse Application</title></head>
    <body>
        <form id="application_form">
            <input name="job_application[first_name]" type="text" />
            <input name="job_application[last_name]" type="text" />
            <input name="job_application[email]" type="email" />
            <input name="job_application[phone]" type="tel" />
            <input name="job_application[location]" type="text" />
            <input name="job_application[resume]" type="file" />
        </form>
    </body>
    </html>
    """
    
    # Set content
    page.set_content(mock_html)
    
    # Create page object
    greenhouse_page = GreenhousePage(page)
    
    # Test filling fields
    test_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1-555-123-4567",
        "country": "Canada"
    }
    
    greenhouse_page.fill_first_name(test_data["first_name"])
    greenhouse_page.fill_last_name(test_data["last_name"])
    greenhouse_page.fill_email(test_data["email"])
    greenhouse_page.fill_phone(test_data["phone"])
    greenhouse_page.fill_country(test_data["country"])
    
    # Verify fields were filled
    assert greenhouse_page.get_first_name_value() == test_data["first_name"]
    assert greenhouse_page.get_last_name_value() == test_data["last_name"]
    assert greenhouse_page.get_email_value() == test_data["email"]
    assert greenhouse_page.get_phone_value() == test_data["phone"]
    
    # Verify fields exist
    assert greenhouse_page.verify_first_name_field()
    assert greenhouse_page.verify_last_name_field()
    assert greenhouse_page.verify_email_field()
    assert greenhouse_page.verify_phone_field()
    assert greenhouse_page.verify_resume_field()


def test_greenhouse_page_fill_application_method(page: Page):
    """Test the convenience method for filling the complete application.
    
    Args:
        page: Playwright page fixture
    """
    # Create a mock HTML page
    mock_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Mock Greenhouse Application</title></head>
    <body>
        <form id="application_form">
            <input name="job_application[first_name]" type="text" />
            <input name="job_application[last_name]" type="text" />
            <input name="job_application[email]" type="email" />
            <input name="job_application[phone]" type="tel" />
            <input name="job_application[location]" type="text" />
            <input name="job_application[resume]" type="file" />
        </form>
    </body>
    </html>
    """
    
    page.set_content(mock_html)
    
    greenhouse_page = GreenhousePage(page)
    
    # Test data
    test_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "phone": "+44-20-1234-5678",
        "country": "United Kingdom"
    }
    
    # Fill application using convenience method
    greenhouse_page.fill_application(
        first_name=test_data["first_name"],
        last_name=test_data["last_name"],
        email=test_data["email"],
        country=test_data["country"],
        phone=test_data["phone"],
        resume_path=TEST_RESUME_PATH
    )
    
    # Verify all fields were filled
    assert greenhouse_page.get_first_name_value() == test_data["first_name"]
    assert greenhouse_page.get_last_name_value() == test_data["last_name"]
    assert greenhouse_page.get_email_value() == test_data["email"]
    assert greenhouse_page.get_phone_value() == test_data["phone"]
    
    # Verify file was attached
    assert greenhouse_page.verify_file_attached()
