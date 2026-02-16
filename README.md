# apply4me

This project specializes in remote job applications to major services like Ashby, Lever or Greenhouse.

## Features

- **Automated Job Applications**: Apply to jobs automatically using Playwright browser automation
- **Greenhouse Support**: Currently supports Greenhouse application tracking system
- **Page Object Model**: Clean, maintainable code structure using the Page Object Model design pattern
- **Dockerized**: Runs in a containerized environment for consistency and portability
- **Comprehensive Tests**: Full test coverage for form filling and file attachments

## Current Capabilities

The application can automatically fill out job applications with:
- First Name
- Last Name
- Email
- Phone Number
- Country/Location
- Resume/CV (PDF file attachment)

## Project Structure

```
apply4me/
├── pages/                  # Page Object Model classes
│   ├── base_page.py       # Base page with common functionality
│   └── greenhouse_page.py # Greenhouse-specific page object
├── tests/                 # Test files
│   └── test_greenhouse.py # Tests for Greenhouse functionality
├── data/                  # Test data files
│   └── test_resume.pdf   # Sample resume for testing
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── pytest.ini           # Pytest configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- OR Python 3.11+ if running locally

### Running with Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the tests:
   ```bash
   docker-compose run apply4me
   ```

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install --with-deps chromium
   ```

2. Run the tests:
   ```bash
   pytest tests/ -v
   ```

## Usage Example

```python
from playwright.sync_api import sync_playwright
from pages.greenhouse_page import GreenhousePage

# Initialize Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Create page object
    greenhouse_page = GreenhousePage(page)
    
    # Open job application
    greenhouse_page.open_job_application("https://job-boards.eu.greenhouse.io/copperco/jobs/4709339101")
    
    # Fill application
    greenhouse_page.fill_application(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        country="United States",
        phone="+1-234-567-8900",
        resume_path="data/test_resume.pdf"
    )
    
    browser.close()
```

## Running Tests

The test suite includes:
- Field verification tests (checking all required fields exist)
- Form filling tests (verifying data is correctly entered)
- File attachment tests (verifying resume upload works)
- Complete application flow tests

Run all tests:
```bash
pytest tests/ -v
```

Run specific test:
```bash
pytest tests/test_greenhouse.py::test_fill_greenhouse_application -v
```

## Development

### Adding Support for New Job Boards

1. Create a new page object class in `pages/` (e.g., `lever_page.py`)
2. Inherit from `BasePage`
3. Define selectors for the job board's form fields
4. Implement methods to fill each field
5. Add tests in `tests/`

### Page Object Model

The Page Object Model (POM) design pattern is used to:
- Separate test logic from page-specific code
- Make tests more maintainable
- Reduce code duplication
- Provide a clear API for interacting with pages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details. 
