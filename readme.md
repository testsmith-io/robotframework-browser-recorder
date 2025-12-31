# Robot Framework Browser Recorder

A Python package that records browser interactions using Playwright's codegen feature and automatically converts them to Robot Framework test cases using the [Browser library](https://marketsquare.github.io/robotframework-browser/Browser.html).

## Features

- 🎥 **Record browser interactions** using Playwright's powerful codegen tool
- 🤖 **Automatic conversion** to Robot Framework test syntax
- 🌐 **Multi-browser support**: Chromium, Firefox, and WebKit
- 🎯 **Simple CLI** for quick test generation
- 📝 **Clean, readable output** with simplified selectors (e.g., `data-test=login` instead of `[data-test="login"]`)

## Installation

### Prerequisites

- Python 3.8 or higher
- Playwright (installed automatically with the package)

### Install the package

```bash
pip install robotframework-browser-recorder
```

### Install Playwright browsers

After installing the package, you need to install Playwright browsers:

```bash
playwright install  # Install all browsers
# OR install specific browsers:
playwright install chromium
playwright install firefox
playwright install webkit
```

### Install Robot Framework Browser library

```bash
pip install robotframework-browser
rfbrowser init
```

## Quick Start

### Basic Recording

Record browser interactions and generate a Robot Framework test:

```bash
rfbrowser-record --url https://example.com
```

This will:
1. Open a browser window with the Playwright inspector (Chromium by default)
2. Navigate to the specified URL
3. Record all your interactions (clicks, typing, etc.)
4. Generate a `recorded_test.robot` file when you close the browser

### Run Your Test

After recording, run your test with:

```bash
robot recorded_test.robot
```

## Usage

### Command Line Interface

```bash
rfbrowser-record [OPTIONS]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--url` | `-u` | Initial URL to navigate to | None |
| `--browser` | `-b` | Browser to use (chromium, firefox, webkit) | chromium |
| `--output` | `-o` | Output file path | recorded_test.robot |
| `--test-name` | `-n` | Name of the test case | Recorded Test |
| `--headless` | | Run browser in headless mode | False |
| `--version` | | Show version | |

### Examples

#### Record with Firefox

```bash
rfbrowser-record --browser firefox --url https://example.com
```

#### Record with custom output file

```bash
rfbrowser-record --url https://example.com --output my_test.robot
```

#### Headless recording

```bash
rfbrowser-record --headless --url https://example.com
```

### Python API

You can also use the recorder programmatically:

```python
from robotframework_browser_recorder import BrowserRecorder

# Create a recorder instance (Chromium by default)
recorder = BrowserRecorder(
    output_file="my_test.robot",
    test_name="My Custom Test",
    url="https://example.com"
)

# Start recording
recorder.record()

# Or use Firefox
recorder_ff = BrowserRecorder(
    browser="firefox",
    output_file="my_test.robot",
    url="https://example.com"
)
recorder_ff.record()
```

### Converting Playwright Code

If you already have Playwright Python code, you can convert it:

```python
from robotframework_browser_recorder import PlaywrightToRobotConverter

playwright_code = """
page.goto("https://example.com")
page.locator("[data-test='login']").click()
page.locator("[data-test='username']").fill("testuser")
page.locator("[data-test='password']").fill("testpass")
page.locator("[data-test='submit']").click()
"""

converter = PlaywrightToRobotConverter()
robot_test = converter.convert(
    playwright_code=playwright_code,
    test_name="Login Test"
)

print(robot_test)
```

## Supported Actions

The converter supports the following Playwright actions:

| Playwright Action | Robot Framework Keyword |
|-------------------|-------------------------|
| `page.goto(url)` | `New Page    url` |
| `page.click(selector)` or `.click()` | `Click    selector` |
| `page.fill(selector, value)` or `.fill()` | `Type Text    selector    value` |
| `page.press(selector, key)` | `Keyboard Key    press    key` |
| `page.check(selector)` | `Check Checkbox    selector` |
| `page.uncheck(selector)` | `Uncheck Checkbox    selector` |
| `page.select_option(selector, value)` | `Select Options By    selector    value    value` |
| `page.hover(selector)` | `Hover    selector` |
| `page.dblclick(selector)` | `Click    selector    clickCount=2` |
| `page.screenshot(path=path)` | `Take Screenshot    path` |
| `page.wait_for_load_state(state)` | `Wait For Load State    state` |

## Example Output

After recording interactions on a website, you'll get a clean Robot Framework test:

```robot
*** Settings ***
Library    Browser


*** Test Cases ***
Login Test
    New Browser    chromium    headless=False
    New Context    viewport={'width': 1920, 'height': 1080}
    New Page    https://example.com
    Click    data-test=nav-sign-in
    Type Text    data-test=email    test@test.nl
    Type Text    data-test=password    SuperSecretPassword!
    Click    data-test=login-submit
```

Notice how selectors are simplified:
- `[data-test="nav-sign-in"]` becomes `data-test=nav-sign-in`
- `[id="submit"]` becomes `id=submit`

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/robotframework-browser-recorder.git
cd robotframework-browser-recorder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install Playwright
playwright install chromium
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black robotframework_browser_recorder/
```

## Troubleshooting

### Playwright not found

If you get an error about Playwright not being installed:

```bash
pip install playwright
playwright install chromium
```

### Browser library not found

Make sure the Robot Framework Browser library is installed:

```bash
pip install robotframework-browser
rfbrowser init chromium
```

### Recording produces no output

Make sure you actually perform some interactions in the browser before closing it. The recorder only captures actions like clicks, typing, navigation, etc.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache License 2.0

## Related Projects

- [Robot Framework](https://robotframework.org/)
- [Robot Framework Browser Library](https://github.com/MarketSquare/robotframework-browser)
- [Playwright](https://playwright.dev/)

## Acknowledgments

This project builds upon the excellent work of:
- The Robot Framework community
- The Playwright team at Microsoft
- The Browser library maintainers
