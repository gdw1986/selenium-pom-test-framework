# run_parallel.py - Parallel test execution with pabot
# Usage: python run_parallel.py [--workers N] [--suite suite_name] [--browser chromium]
import subprocess
import argparse
import sys

SUITES = {
    "login":    "tests/test_login.robot",
    "alert":    "tests/test_alert.robot",
    "dropdown": "tests/test_dropdown.robot",
    "upload":   "tests/test_file_upload.robot",
    "comment":  "tests/test_comments.robot",
    "window":   "tests/test_windows.robot",
    "all":      None,
}

def run_parallel(suite="all", workers=4, browser="chromium", headless=False):
    robot_args = [
        "pabot",
        "--outputdir", "results_parallel",
        "-v", f"BROWSER:{browser}",
        "-v", f"DEFAULT_HEADLESS:{str(headless).lower()}",
        "--processes", str(workers),
    ]

    if suite == "all":
        robot_args += list(SUITES.values())[:-1]
    else:
        robot_args.append(SUITES.get(suite, "tests/"))

    print(f"Running: pabot {' '.join(robot_args[1:])}")
    return subprocess.run(["pabot"] + robot_args[1:]).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel test runner (pabot)")
    parser.add_argument("--workers", "-w", default=4, type=int,
                        help="Number of parallel workers (default: 4)")
    parser.add_argument("--suite", "-s", default="all",
                        choices=list(SUITES.keys()))
    parser.add_argument("--browser", "-b", default="chromium",
                        choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    sys.exit(run_parallel(args.suite, args.workers, args.browser, args.headless))
