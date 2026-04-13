# run_allure.py - Run tests and generate Allure report
# Usage: python run_allure.py [--serve] [--suite suite_name] [--browser chromium]
import subprocess
import argparse
import shutil
import sys
import os

def main(suite="all", browser="chromium", headless=False, serve=False):
    allure_results = "allure-results"
    allure_report   = "allure-report"
    results_dir     = "results"

    # Clean old results
    for d in [allure_results, allure_report]:
        if os.path.exists(d):
            shutil.rmtree(d)
    os.makedirs(allure_results, exist_ok=True)

    # Run robot
    robot_args = [
        "robot",
        "--outputdir", results_dir,
        "-o", "output.xml",
        "-r", "report.html",
        "-l", "log.html",
        "-v", f"BROWSER:{browser}",
        "-v", f"DEFAULT_HEADLESS:{str(headless).lower()}",
    ]

    SUITES = {
        "login": "tests/test_login.robot",
        "alert": "tests/test_alert.robot",
        "dropdown": "tests/test_dropdown.robot",
        "upload": "tests/test_file_upload.robot",
        "comment": "tests/test_comments.robot",
        "window": "tests/test_windows.robot",
    }
    if suite == "all":
        robot_args += list(SUITES.values())
    else:
        robot_args.append(SUITES.get(suite, "tests/"))

    print(f"Running tests...")
    result = subprocess.run(["robot"] + robot_args[1:])
    if result.returncode != 0:
        print("Tests failed (non-zero exit), still generating report...")

    # Generate Allure report
    try:
        subprocess.run(
            ["allure", "generate", allure_results, "-o", allure_report, "--clean"],
            check=True,
        )
    except FileNotFoundError:
        print("ERROR: 'allure' CLI not found.")
        print("Install: https://allure.qameta.io/")
        print("  macOS: brew install allure")
        print("  Windows: scoop install allure")
        sys.exit(1)

    if serve:
        subprocess.run(["allure", "serve", allure_results])
    else:
        report_path = os.path.abspath(f"{allure_report}/index.html")
        print(f"\nReport generated: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests and generate Allure report")
    parser.add_argument("--suite", "-s", default="all")
    parser.add_argument("--browser", "-b", default="chromium")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--serve", action="store_true", help="Serve report locally")
    args = parser.parse_args()
    main(args.suite, args.browser, args.headless, args.serve)
