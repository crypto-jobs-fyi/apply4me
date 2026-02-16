"""Example application for filling Greenhouse job applications.

This script demonstrates how to use the GreenhousePage class to automate
filling out a job application on Greenhouse.
"""
import os
from playwright.sync_api import sync_playwright
from pages.greenhouse_page import GreenhousePage


def main():
    """Main function to demonstrate job application automation."""
    # Configuration
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    
    # Applicant data
    applicant_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "country": "United States",
        "phone": "+1-234-567-8900"
    }
    
    # Resume path
    resume_path = os.path.join(os.path.dirname(__file__), "data", "test_resume.pdf")
    
    # Launch browser and fill application
    with sync_playwright() as p:
        # Launch browser (set headless=False to see the browser)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Create page object
        greenhouse_page = GreenhousePage(page)
        
        print(f"Opening job application: {job_url}")
        greenhouse_page.open_job_application(job_url)
        
        print("Filling application form...")
        greenhouse_page.fill_application(
            first_name=applicant_data["first_name"],
            last_name=applicant_data["last_name"],
            email=applicant_data["email"],
            country=applicant_data["country"],
            phone=applicant_data["phone"],
            resume_path=resume_path
        )
        
        print("Application form filled successfully!")
        print("\nVerifying fields...")
        
        # Verify fields
        assert greenhouse_page.get_first_name_value() == applicant_data["first_name"]
        assert greenhouse_page.get_last_name_value() == applicant_data["last_name"]
        assert greenhouse_page.get_email_value() == applicant_data["email"]
        assert greenhouse_page.get_phone_value() == applicant_data["phone"]
        
        print("All fields verified!")
        print("\nPress Enter to close the browser...")
        input()
        
        browser.close()


if __name__ == "__main__":
    main()
