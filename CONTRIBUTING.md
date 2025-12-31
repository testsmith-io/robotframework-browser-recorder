# Contributing to Robot Framework Browser Recorder

Thank you for your interest in contributing to Robot Framework Browser Recorder!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/robotframework-browser-recorder.git
   cd robotframework-browser-recorder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   playwright install
   ```

4. **Install Robot Framework Browser library**
   ```bash
   pip install robotframework-browser
   rfbrowser init
   ```

## Running Tests

Run the test suite with pytest:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=robotframework_browser_recorder --cov-report=html
```

## Code Style

This project uses Black for code formatting and Flake8 for linting.

Format your code:
```bash
black robotframework_browser_recorder/
```

Check linting:
```bash
flake8 robotframework_browser_recorder/
```

## Type Checking

Run mypy for type checking:
```bash
mypy robotframework_browser_recorder/
```

## Making Changes

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Add or update tests as needed
4. Run the test suite to ensure everything passes
5. Format your code with Black
6. Submit a pull request

## Adding New Playwright Action Conversions

To add support for a new Playwright action:

1. Add the action name to `action_mappings` in `PlaywrightToRobotConverter.__init__()`
2. Create a converter method (e.g., `_convert_new_action()`)
3. Add parsing logic in `_parse_playwright_code()` if needed
4. Add tests in `tests/test_converter.py`

## Project Structure

```
robotframework-browser-recorder/
├── robotframework_browser_recorder/
│   ├── __init__.py
│   ├── recorder.py              # Main recorder class
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py              # CLI interface
│   ├── converter/
│   │   ├── __init__.py
│   │   └── playwright_to_robot.py  # Conversion logic
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_converter.py
├── examples/
│   ├── example_test.robot
│   ├── playwright_example.py
│   └── recorder_example.py
├── pyproject.toml
├── setup.py
├── readme.md
└── requirements.txt
```

## Questions?

Feel free to open an issue if you have questions or need help!
