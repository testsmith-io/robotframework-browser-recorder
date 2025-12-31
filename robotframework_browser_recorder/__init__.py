"""Robot Framework Browser Recorder.

A tool to record browser interactions using Playwright codegen and convert them
to Robot Framework test cases using the Browser library.
"""

__version__ = "0.1.0"
__author__ = "Robot Framework Browser Recorder Contributors"

from robotframework_browser_recorder.recorder import BrowserRecorder
from robotframework_browser_recorder.converter.playwright_to_robot import PlaywrightToRobotConverter

__all__ = ["BrowserRecorder", "PlaywrightToRobotConverter"]
