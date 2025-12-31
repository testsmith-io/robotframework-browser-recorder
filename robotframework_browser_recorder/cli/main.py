"""Main CLI entry point for Robot Framework Browser Recorder."""

import argparse
import sys
from robotframework_browser_recorder.recorder import BrowserRecorder


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Record browser interactions and generate Robot Framework tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record interactions on a specific URL
  rfbrowser-record --url https://example.com

  # Record with Firefox
  rfbrowser-record --browser firefox --url https://example.com

  # Record with custom output file
  rfbrowser-record --url https://example.com --output my_test.robot

  # Record in headless mode
  rfbrowser-record --url https://example.com --headless
        """,
    )

    parser.add_argument(
        "--url",
        "-u",
        type=str,
        help="Initial URL to navigate to",
        default=None,
    )

    parser.add_argument(
        "--browser",
        "-b",
        type=str,
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser to use for recording (default: chromium)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="recorded_test.robot",
        help="Output file path for the Robot Framework test (default: recorded_test.robot)",
    )

    parser.add_argument(
        "--test-name",
        "-n",
        type=str,
        default="Recorded Test",
        help="Name of the test case (default: Recorded Test)",
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    recorder = BrowserRecorder(
        browser=args.browser,
        output_file=args.output,
        test_name=args.test_name,
        url=args.url,
    )

    try:
        output_file = recorder.record(headless=args.headless)
        print("\nSuccess! You can now run your test with:")
        print(f"  robot {output_file}")

    except KeyboardInterrupt:
        print("\nRecording cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
