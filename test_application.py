import os
import sys
from playwright.sync_api import sync_playwright, expect
from pages.greenhouse_page import GreenhousePage

# Test data as requested
TEST_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "country": "United States",
    "phone": "+1-234-567-8900"
}

def run_test(headed=False):
    """Run a Playwright test to fill the Greenhouse application."""
    job_url = "https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101"
    resume_path = os.path.join(os.path.dirname(__file__), "data", "test_resume.pdf")

    print(f"Starting test ({'headed' if headed else 'headless'} mode)...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context()
        page = context.new_page()
        
        # Initialize Page Object
        greenhouse_page = GreenhousePage(page)
        
        try:
            # 1. Open URL
            print(f"Navigating to: {job_url}")
            greenhouse_page.open_job_application(job_url)
            
            # 2. Input Data
            print("Inputting test data...")
            greenhouse_page.fill_application(
                first_name=TEST_DATA["first_name"],
                last_name=TEST_DATA["last_name"],
                email=TEST_DATA["email"],
                country=TEST_DATA["country"],
                phone=TEST_DATA["phone"],
                resume_path=resume_path
            )
            
            # 3. Verify (using Playwright web-first assertions)
            print("Verifying input values...")
            expect(page.locator(GreenhousePage.FIRST_NAME_INPUT).first).to_have_value(TEST_DATA["first_name"])
            expect(page.locator(GreenhousePage.LAST_NAME_INPUT).first).to_have_value(TEST_DATA["last_name"])
            expect(page.locator(GreenhousePage.EMAIL_INPUT).first).to_have_value(TEST_DATA["email"])
            
            print("✓ Test passed successfully!")
            
            if headed:
                print("Headed mode: Keeping browser open for 5 seconds...")
                page.wait_for_timeout(5000)
                
        except Exception as e:
            print(f"✗ Test failed: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    # Check for --headed flag in command line arguments
    headed_mode = "--headed" in sys.argv
    run_test(headed=headed_mode)
