"""Greenhouse job application page object."""
from pages.base_page import BasePage
from playwright.sync_api import Page


class GreenhousePage(BasePage):
    """Page object for Greenhouse job application forms."""

    # Selectors for form fields - supports both boards.greenhouse.io and job-boards.eu.greenhouse.io
    FIRST_NAME_INPUT = 'input#first_name, input[name="job_application[first_name]"]'
    LAST_NAME_INPUT = 'input#last_name, input[name="job_application[last_name]"]'
    EMAIL_INPUT = 'input#email, input[name="job_application[email]"]'
    PHONE_INPUT = 'input#phone, input[name="job_application[phone]"]'
    RESUME_INPUT = 'input#resume, input[type="file"][name="job_application[resume]"]'
    
    # Country/Location field - may vary by job posting
    COUNTRY_INPUT = 'input#country, input[name="job_application[location]"]'
    
    # Alternative selectors
    LOCATION_INPUT = 'input[autocomplete="address-level2"]'

    def __init__(self, page: Page):
        """Initialize Greenhouse page.
        
        Args:
            page: Playwright page object
        """
        super().__init__(page)

    def open_job_application(self, job_url: str):
        """Open a Greenhouse job application page.
        
        Args:
            job_url: The URL of the job posting
        """
        self.navigate_to(job_url)
        # Wait for the network to be idle to ensure React/etc. has finished loading
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            # If networkidle fails, just continue
            pass

    def fill_first_name(self, first_name: str):
        """Fill the first name field.
        
        Args:
            first_name: The first name to enter
        """
        self.fill_input(self.FIRST_NAME_INPUT, first_name)

    def fill_last_name(self, last_name: str):
        """Fill the last name field.
        
        Args:
            last_name: The last name to enter
        """
        self.fill_input(self.LAST_NAME_INPUT, last_name)

    def fill_email(self, email: str):
        """Fill the email field.
        
        Args:
            email: The email address to enter
        """
        self.fill_input(self.EMAIL_INPUT, email)

    def fill_phone(self, phone: str):
        """Fill the phone number field.
        
        Args:
            phone: The phone number to enter
        """
        self.fill_input(self.PHONE_INPUT, phone)

    def fill_country(self, country: str):
        """Fill the country/location field.
        
        Args:
            country: The country or location to enter
        """
        # Try the first selector
        try:
            self.fill_input(self.COUNTRY_INPUT, country)
        except Exception:
            # Try alternative location selector if first fails
            try:
                self.fill_input(self.LOCATION_INPUT, country)
            except Exception:
                # If both fail, log but continue
                print(f"Warning: Could not find country/location field")

    def attach_resume(self, file_path: str):
        """Attach a resume file.
        
        Args:
            file_path: Path to the resume file (PDF)
        """
        self.upload_file(self.RESUME_INPUT, file_path)

    def fill_application(self, first_name: str, last_name: str, email: str, 
                         country: str, phone: str, resume_path: str):
        """Fill out the complete job application form.
        
        Args:
            first_name: First name
            last_name: Last name
            email: Email address
            country: Country or location
            phone: Phone number
            resume_path: Path to resume PDF file
        """
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.fill_phone(phone)
        self.fill_country(country)
        self.attach_resume(resume_path)

    def verify_first_name_field(self) -> bool:
        """Verify first name field is present.
        
        Returns:
            True if field is present
        """
        return self.page.locator(self.FIRST_NAME_INPUT).is_visible()

    def verify_last_name_field(self) -> bool:
        """Verify last name field is present.
        
        Returns:
            True if field is present
        """
        return self.page.locator(self.LAST_NAME_INPUT).is_visible()

    def verify_email_field(self) -> bool:
        """Verify email field is present.
        
        Returns:
            True if field is present
        """
        return self.page.locator(self.EMAIL_INPUT).is_visible()

    def verify_phone_field(self) -> bool:
        """Verify phone field is present.
        
        Returns:
            True if field is present
        """
        return self.page.locator(self.PHONE_INPUT).is_visible()

    def verify_resume_field(self) -> bool:
        """Verify resume upload field is present.
        
        Returns:
            True if field is present
        """
        return self.page.locator(self.RESUME_INPUT).count() > 0

    def get_first_name_value(self) -> str:
        """Get the current value of the first name field.
        
        Returns:
            The value in the first name field
        """
        return self.page.locator(self.FIRST_NAME_INPUT).input_value()

    def get_last_name_value(self) -> str:
        """Get the current value of the last name field.
        
        Returns:
            The value in the last name field
        """
        return self.page.locator(self.LAST_NAME_INPUT).input_value()

    def get_email_value(self) -> str:
        """Get the current value of the email field.
        
        Returns:
            The value in the email field
        """
        return self.page.locator(self.EMAIL_INPUT).input_value()

    def get_phone_value(self) -> str:
        """Get the current value of the phone field.
        
        Returns:
            The value in the phone field
        """
        return self.page.locator(self.PHONE_INPUT).input_value()

    def verify_file_attached(self) -> bool:
        """Verify that a file has been attached.
        
        Returns:
            True if a file is attached
        """
        # Check if the file input has files
        try:
            # Use first() in case multiple elements match
            return self.page.locator(self.RESUME_INPUT).first.evaluate("el => el.files.length > 0")
        except Exception:
            # Fallback to checking input_value if evaluate fails
            try:
                val = self.page.locator(self.RESUME_INPUT).first.input_value()
                return len(val) > 0
            except Exception:
                return False
