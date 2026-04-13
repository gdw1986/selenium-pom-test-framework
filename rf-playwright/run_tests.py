# run_tests.py - Robot Framework test runner
# Usage: python run_tests.py [--suite suite_name] [--browser chromium|firefox|webkit] [--headless]
import subprocess
import argparse
import sys
import urllib.request

SUITES = {
    "login":   "tests/test_login.robot",
    "alert":   "tests/test_alert.robot",
    "dropdown": "tests/test_dropdown.robot",
    "upload":  "tests/test_file_upload.robot",
    "comment": "tests/test_comments.robot",
    "window":  "tests/test_windows.robot",
    "tabs":    "tests/test_tabs.robot",
    "all":     None,
}

def check_server():
    """Check if the test page HTTP server is running."""
    try:
        urllib.request.urlopen("http://localhost:8080/test_page.html", timeout=2)
        return True
    except Exception:
        return False


def run_tests(suite="all", browser="chromium", headless=False, verbose=False):
    robot_args = [
        "robot",
        "--outputdir", "results",
        "--loglevel", "INFO",
        "-v", f"BROWSER:{browser}",
        "-v", f"HEADLESS:{str(headless).lower()}",
    ]

    if verbose:
        robot_args.append("--verbose")

    if suite == "all":
        robot_args += list(SUITES.values())[:-1]  # exclude "all" key
    else:
        if suite not in SUITES:
            print(f"Unknown suite: {suite}. Options: {', '.join(SUITES)}")
            sys.exit(1)
        robot_args.append(SUITES[suite])

    print(f"Running: robot {' '.join(robot_args[1:])}")
    return subprocess.run(["robot"] + robot_args[1:]).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RF Playwright Test Runner")
    parser.add_argument("--suite", "-s", default="all",
                        choices=list(SUITES.keys()),
                        help="Test suite (default: all)")
    parser.add_argument("--browser", "-b", default="chromium",
                        choices=["chromium", "firefox", "webkit"],
                        help="Browser (default: chromium)")
    parser.add_argument("--headless", action="store_true",
                        help="Run in headless mode")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if not check_server():
        print("=" * 60)
        print("ERROR: http://localhost:8080/test_page.html not reachable.")
        print()
        print("Start the HTTP server first:")
        print("  cd rf-playwright-test-framework")
        print("  python -m http.server 8080")
        print("=" * 60)
        sys.exit(1)

    sys.exit(run_tests(args.suite, args.browser, args.headless, args.verbose))
