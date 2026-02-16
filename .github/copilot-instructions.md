# Copilot Instructions for apply4me

## Project Overview
apply4me is a Python-based browser automation tool that specializes in remote job applications to major application tracking systems like Greenhouse, Lever, and Ashby. The project uses Playwright for browser automation and follows the Page Object Model (POM) design pattern.

## Project Structure
```
apply4me/
├── pages/                      # Page Object Model classes
│   ├── base_page.py           # Base page with common functionality
│   └── greenhouse_page.py     # Greenhouse-specific implementation
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest configuration
│   ├── test_page_objects.py  # Unit tests with mock forms
│   └── test_greenhouse.py    # Integration tests with real URLs
├── data/                      # Test data files
│   └── test_resume.pdf       # Sample resume for testing
├── apply_greenhouse.py        # Example application script
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest settings
└── .github/                  # GitHub configuration
    └── copilot-instructions.md
```

## Technology Stack
- **Language**: Python 3.11+
- **Browser Automation**: Playwright 1.40.0
- **Testing**: pytest 7.4.3, pytest-playwright 0.4.3
- **Containerization**: Docker with Docker Compose

## Build, Test, and Run

### Docker (Recommended)
```bash
# Build the Docker image
docker-compose build

# Run tests
docker-compose run apply4me

# Run specific tests
docker-compose run apply4me pytest tests/test_page_objects.py -v
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers with dependencies
playwright install --with-deps chromium

# Run all tests
pytest tests/ -v

# Run unit tests only (no network required)
pytest tests/test_page_objects.py -v

# Run integration tests (requires network access)
pytest tests/test_greenhouse.py -v

# Run specific test
pytest tests/test_greenhouse.py::test_fill_greenhouse_application -v
```

## Coding Standards

### Python Style
- Follow PEP 8 style guide for Python code
- Use descriptive variable and function names
- Use type hints where appropriate
- Keep functions focused on single responsibility

### Page Object Model Pattern
- **ALWAYS** use the Page Object Model design pattern for browser automation
- **BasePage** contains common functionality shared across all page objects
- Each job board has its own page object class (e.g., GreenhousePage, LeverPage)
- All page objects must inherit from BasePage
- Define selectors as class constants at the top of each page object
- Methods should be named clearly (e.g., `fill_first_name()`, `verify_email_field()`)

### Selector Naming Convention
- Use UPPERCASE_WITH_UNDERSCORES for CSS selector constants
- Name selectors after their purpose (e.g., `FIRST_NAME_INPUT`, `SUBMIT_BUTTON`)
- Greenhouse forms use `job_application[field_name]` naming pattern for input fields

### Testing Practices
- Use pytest with pytest-playwright plugin for browser automation testing
- Separate unit tests (with mock HTML) from integration tests (with real URLs)
- Unit tests should not require network access
- Integration tests should verify end-to-end workflows
- Add tests for any new page objects or methods
- Test file naming: `test_*.py`
- Test function naming: `test_*`

### File Organization
- Page objects go in `pages/` directory
- Test files go in `tests/` directory
- Test data files go in `data/` directory
- Example scripts go in the root directory

## Adding Support for New Job Boards

To add a new job board (e.g., Lever, Ashby):

1. Create a new page object in `pages/` (e.g., `lever_page.py`)
2. Inherit from `BasePage`
3. Define CSS selectors as class constants
4. Implement methods to fill each field
5. Add a convenience method like `fill_application()` for filling all fields at once
6. Create corresponding test file in `tests/` (e.g., `test_lever.py`)
7. Write both unit tests (mock HTML) and integration tests (real URLs)

Example structure:
```python
from pages.base_page import BasePage

class LeverPage(BasePage):
    # Selectors
    FIRST_NAME_INPUT = 'input[name="first_name"]'
    LAST_NAME_INPUT = 'input[name="last_name"]'
    # ... other selectors
    
    def fill_first_name(self, name):
        self.fill_input(self.FIRST_NAME_INPUT, name)
    
    def fill_application(self, **kwargs):
        # Fill all fields
        pass
```

## Docker Configuration
- Playwright requires `playwright install --with-deps` flag for browser dependencies in Docker
- The Dockerfile uses Python 3.11-slim as the base image
- All Playwright browsers must be installed during image build

## Security Guidelines
- Never commit sensitive data (credentials, API keys) to the repository
- Use environment variables for any configuration that varies between environments
- Validate all user inputs before processing
- Be respectful of job board rate limits and terms of service

## Common Patterns

### Working with Form Fields
- Use `fill_input()` from BasePage for text inputs
- Use `click_element()` for buttons and clickable elements
- Use `upload_file()` for file attachments
- Use `wait_for_element()` to ensure elements are present before interaction

### Verification Methods
- Implement `verify_*_field()` methods to check if fields exist
- Implement `get_*_value()` methods to retrieve field values for assertions

## Notes
- Integration tests may fail in restricted network environments (e.g., CI/CD without internet access)
- Unit tests should always pass regardless of network conditions
- When running tests, Playwright traces are retained on failure for debugging (see pytest.ini)
