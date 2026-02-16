"""Tests for Greenhouse job application page."""
import pytest
import os
from playwright.sync_api import Page, expect
from pages.greenhouse_page import GreenhousePage


# Test data
TEST_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "country": "United States",
    "phone": "+1-234-567-8900"
}

# Path to test resume
TEST_RESUME_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_resume.pdf")


@pytest.fixture
def greenhouse_page(page: Page):
    """Create a GreenhousePage instance.
    
    Args:
        page: Playwright page fixture
        
    Returns:
        GreenhousePage instance
    """
    return GreenhousePage(page)


def test_greenhouse_form_fields_exist(page: Page, greenhouse_page: GreenhousePage):
    """Test that all required form fields exist on Greenhouse job page.
    
    Args:
        page: Playwright page fixture
        greenhouse_page: GreenhousePage fixture
    """
    # Open the example Greenhouse job posting
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    greenhouse_page.open_job_application(job_url)
    
    # Verify all required fields are present
    assert greenhouse_page.verify_first_name_field(), "First name field not found"
    assert greenhouse_page.verify_last_name_field(), "Last name field not found"
    assert greenhouse_page.verify_email_field(), "Email field not found"
    assert greenhouse_page.verify_phone_field(), "Phone field not found"
    assert greenhouse_page.verify_resume_field(), "Resume upload field not found"


def test_fill_greenhouse_application(page: Page, greenhouse_page: GreenhousePage):
    """Test filling out a Greenhouse job application form.
    
    Args:
        page: Playwright page fixture
        greenhouse_page: GreenhousePage fixture
    """
    # Open the example Greenhouse job posting
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    greenhouse_page.open_job_application(job_url)
    
    # Fill in all fields
    greenhouse_page.fill_first_name(TEST_DATA["first_name"])
    greenhouse_page.fill_last_name(TEST_DATA["last_name"])
    greenhouse_page.fill_email(TEST_DATA["email"])
    greenhouse_page.fill_phone(TEST_DATA["phone"])
    greenhouse_page.fill_country(TEST_DATA["country"])
    
    # Verify the fields were filled correctly
    assert greenhouse_page.get_first_name_value() == TEST_DATA["first_name"], \
        f"First name not filled correctly"
    assert greenhouse_page.get_last_name_value() == TEST_DATA["last_name"], \
        f"Last name not filled correctly"
    assert greenhouse_page.get_email_value() == TEST_DATA["email"], \
        f"Email not filled correctly"
    assert greenhouse_page.get_phone_value() == TEST_DATA["phone"], \
        f"Phone not filled correctly"


def test_attach_resume(page: Page, greenhouse_page: GreenhousePage):
    """Test attaching a resume file to Greenhouse application.
    
    Args:
        page: Playwright page fixture
        greenhouse_page: GreenhousePage fixture
    """
    # Verify test resume file exists
    assert os.path.exists(TEST_RESUME_PATH), f"Test resume not found at {TEST_RESUME_PATH}"
    
    # Open the example Greenhouse job posting
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    greenhouse_page.open_job_application(job_url)
    
    # Attach resume
    greenhouse_page.attach_resume(TEST_RESUME_PATH)
    
    # Verify file was attached
    assert greenhouse_page.verify_file_attached(), "Resume file not attached"


def test_complete_application_flow(page: Page, greenhouse_page: GreenhousePage):
    """Test the complete flow of filling out a Greenhouse application.
    
    Args:
        page: Playwright page fixture
        greenhouse_page: GreenhousePage fixture
    """
    # Verify test resume file exists
    assert os.path.exists(TEST_RESUME_PATH), f"Test resume not found at {TEST_RESUME_PATH}"
    
    # Open the example Greenhouse job posting
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    greenhouse_page.open_job_application(job_url)
    
    # Use the convenience method to fill all fields
    greenhouse_page.fill_application(
        first_name=TEST_DATA["first_name"],
        last_name=TEST_DATA["last_name"],
        email=TEST_DATA["email"],
        country=TEST_DATA["country"],
        phone=TEST_DATA["phone"],
        resume_path=TEST_RESUME_PATH
    )
    
    # Verify all fields were filled
    assert greenhouse_page.get_first_name_value() == TEST_DATA["first_name"]
    assert greenhouse_page.get_last_name_value() == TEST_DATA["last_name"]
    assert greenhouse_page.get_email_value() == TEST_DATA["email"]
    assert greenhouse_page.get_phone_value() == TEST_DATA["phone"]
    
    # Verify file was attached
    assert greenhouse_page.verify_file_attached(), "Resume file not attached"
