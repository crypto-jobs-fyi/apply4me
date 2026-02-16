# Architecture Overview

## Project Structure
```
apply4me/
├── pages/                      # Page Object Model
│   ├── __init__.py            # Package initialization
│   ├── base_page.py           # Base page with common functionality
│   └── greenhouse_page.py     # Greenhouse-specific implementation
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest configuration
│   ├── test_page_objects.py  # Unit tests (mock forms)
│   └── test_greenhouse.py    # Integration tests (real URLs)
├── data/                      # Test data
│   └── test_resume.pdf       # Sample resume for testing
├── apply_greenhouse.py        # Example application script
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
└── pytest.ini               # Pytest settings
```

## Architecture

```
┌─────────────────────────────────────────────┐
│         Greenhouse Application              │
│         (apply_greenhouse.py)               │
└─────────────────┬───────────────────────────┘
                  │
                  │ uses
                  ↓
┌─────────────────────────────────────────────┐
│         Page Object Model                   │
├─────────────────────────────────────────────┤
│  BasePage (base_page.py)                   │
│  - navigate_to()                           │
│  - fill_input()                            │
│  - click_element()                         │
│  - upload_file()                           │
│  - wait_for_element()                      │
├─────────────────────────────────────────────┤
│  GreenhousePage (greenhouse_page.py)       │
│  - open_job_application()                  │
│  - fill_first_name()                       │
│  - fill_last_name()                        │
│  - fill_email()                            │
│  - fill_phone()                            │
│  - fill_country()                          │
│  - attach_resume()                         │
│  - fill_application() [convenience]        │
│  - verify_*_field()                        │
│  - get_*_value()                           │
└─────────────────┬───────────────────────────┘
                  │
                  │ controls
                  ↓
┌─────────────────────────────────────────────┐
│         Playwright Browser                  │
│         (Chromium/Firefox/WebKit)          │
└─────────────────────────────────────────────┘
```

## Design Patterns

### Page Object Model (POM)
- **BasePage**: Contains common functionality used by all page objects
- **GreenhousePage**: Greenhouse-specific implementation with selectors and methods
- **Benefits**: 
  - Separation of concerns
  - Reusable code
  - Easy maintenance
  - Clear API for tests

### Inheritance
- GreenhousePage extends BasePage
- Future page objects (Lever, Ashby) will also extend BasePage

## Features Implemented

### Form Fields Supported
- ✅ First Name
- ✅ Last Name  
- ✅ Email
- ✅ Phone
- ✅ Country/Location
- ✅ Resume/CV (PDF attachment)

### Capabilities
- ✅ Fill individual fields
- ✅ Fill complete application (convenience method)
- ✅ Verify field presence
- ✅ Verify field values
- ✅ File attachment verification
- ✅ Dockerized environment
- ✅ Comprehensive test suite

## Testing Strategy

### Unit Tests (test_page_objects.py)
- Test POM structure
- Test methods with mock HTML forms
- No external dependencies
- Fast execution

### Integration Tests (test_greenhouse.py)
- Test with real Greenhouse URLs
- Verify end-to-end workflow
- Requires network access

## Usage

### Standalone Script
```python
from playwright.sync_api import sync_playwright
from pages.greenhouse_page import GreenhousePage

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    greenhouse = GreenhousePage(page)
    
    greenhouse.open_job_application(job_url)
    greenhouse.fill_application(...)
```

### Docker
```bash
docker-compose build
docker-compose run apply4me
```

### Direct Execution
```bash
python apply_greenhouse.py
```

## Future Extensions

To add support for other job boards:

1. Create new page object (e.g., `lever_page.py`)
2. Extend BasePage
3. Define selectors for the specific job board
4. Implement filling methods
5. Add tests

Example:
```python
class LeverPage(BasePage):
    FIRST_NAME_INPUT = 'input[name="first_name"]'
    # ... other selectors
    
    def fill_first_name(self, name):
        self.fill_input(self.FIRST_NAME_INPUT, name)
```
