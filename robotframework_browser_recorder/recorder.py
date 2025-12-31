"""Browser interaction recorder using Playwright codegen."""

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Optional
from robotframework_browser_recorder.converter.playwright_to_robot import PlaywrightToRobotConverter


class BrowserRecorder:
    """Record browser interactions and convert to Robot Framework tests."""

    def __init__(
        self,
        browser: str = "chromium",
        output_file: Optional[str] = None,
        test_name: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """Initialize the browser recorder.

        Args:
            browser: Browser to use (chromium, firefox, webkit)
            output_file: Path to save the Robot Framework test file
            test_name: Name of the test case
            url: Initial URL to navigate to
        """
        self.browser = browser
        self.output_file = output_file or "recorded_test.robot"
        self.test_name = test_name or "Recorded Test"
        self.url = url
        self.converter = PlaywrightToRobotConverter()

    def record(self) -> str:
        """Start recording browser interactions.

        Returns:
            Path to the generated Robot Framework test file
        """
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            cmd = [
                "playwright",
                "codegen",
                "--target",
                "python",
                "-b",
                self.browser,
                "-o",
                tmp_path,
            ]

            if self.url:
                cmd.append(self.url)

            print(f"Starting Playwright codegen with command: {' '.join(cmd)}")
            print(f"Recording to temporary file: {tmp_path}")
            print("\nPerform your browser interactions in the opened browser window.")
            print("Close the browser window when you're done recording.\n")

            subprocess.run(cmd, check=True)

            with open(tmp_path, "r") as f:
                playwright_code = f.read()

            if not playwright_code.strip():
                raise ValueError("No code was recorded. Please perform some interactions.")

            robot_test = self.converter.convert(
                playwright_code=playwright_code,
                test_name=self.test_name,
            )

            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                f.write(robot_test)

            print(f"\nRecording complete! Robot Framework test saved to: {output_path}")
            return str(output_path)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
