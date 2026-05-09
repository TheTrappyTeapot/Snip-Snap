"""Test runner and report generator for all automated tests."""

import pytest
import sys
import os
import csv
from datetime import datetime
from pathlib import Path


def get_test_config():
    """Get test configuration from CLI or user input.
    
    Returns:
        tuple: (test_range, test_page) where:
            - test_range: "q" (quick, skip selenium) or "f" (full)
            - test_page: "." (all) or specific test file name
    """
    # Try to get from command line arguments first
    if len(sys.argv) > 2:
        test_range = sys.argv[1].lower()
        test_page = sys.argv[2].lower()
    elif len(sys.argv) > 1:
        print(f"Usage: python test_app.py <test_range> <test_page>")
        print(f"       test_range: 'q' (quick) or 'f' (full)")
        print(f"       test_page:  '.' (all) or specific test file name")
        sys.exit(1)
    else:
        # Interactive mode
        print("\n" + "="*60)
        print("SNIP-SNAP TEST RUNNER")
        print("="*60)
        print("\nTest Range:")
        print("  q - Quick (skip slow selenium tests)")
        print("  f - Full (all tests including selenium)")
        test_range = input("\nEnter test range (q/f): ").lower().strip()
        
        print("\nTest Page:")
        print("  . - All test files")
        print("  test_welcome_page")
        print("  test_login_page")
        print("  test_signup_page")
        print("  test_my_profile_page")
        print("  test_barber_dashboard_page")
        print("  test_barber_profile_page")
        print("  test_barbershop_page")
        print("  test_interactive_map_page (contains selenium tests)")
        print("  test_navbar (contains selenium tests)")
        print("  test_review_widget")
        test_page = input("\nEnter test page (. or name): ").lower().strip()
    
    # Validate inputs
    if test_range not in ('q', 'f'):
        print("Error: test_range must be 'q' or 'f'")
        sys.exit(1)
    
    return test_range, test_page


def get_test_files_to_run(test_dir, test_page, skip_selenium=False):
    """Determine which test files to run.
    
    Args:
        test_dir: Path to test directory
        test_page: "." for all, or specific test file name
        skip_selenium: Skip selenium tests if True
    
    Returns:
        list: List of test files to run
    """
    # All available test files
    all_tests = [
        "test_welcome_page.py",
        "test_login_page.py",
        "test_signup_page.py",
        "test_my_profile_page.py",
        "test_barber_dashboard_page.py",
        "test_barber_profile_page.py",
        "test_barbershop_page.py",
        "test_interactive_map_page.py",  # Contains selenium tests
        "test_review_widget.py",
        "test_discover_page.py",
        "test_navbar.py",  # Contains navbar and role-based tests
    ]
    
    # Selenium test file
    selenium_tests = ["test_interactive_map_page.py", "test_navbar.py"]
    
    # Determine which tests to include
    if test_page == ".":
        # All tests
        tests_to_run = all_tests
    else:
        # Specific test file - add .py if not present
        if not test_page.endswith(".py"):
            test_page = test_page + ".py"
        
        # Check if test file exists
        test_file = test_dir / test_page
        if test_file.exists():
            tests_to_run = [test_page]
        else:
            print(f"Error: Test file '{test_page}' not found in {test_dir}")
            sys.exit(1)
    
    # Filter out selenium tests if quick mode
    if skip_selenium:
        tests_to_run = [t for t in tests_to_run if t not in selenium_tests]
    
    return [str(test_dir / t) for t in tests_to_run]


class ResultCollector:
    """Custom pytest plugin to collect test results (not a test class)."""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0
    
    def pytest_runtest_logreport(self, report):
        """Collect test results as pytest runs them."""
        if report.when == "call":
            skip_reason = None
            
            # Capture skip reason from various sources
            if report.outcome == "skipped":
                try:
                    # For pytest.skip(), the skip reason is in report.longrepr
                    # Format is typically: "path/to/file.py:linenum: skip_message"
                    if hasattr(report, 'longrepr') and report.longrepr:
                        longrepr_str = str(report.longrepr)
                        # Split by ": " and extract the skip message
                        # Typically format is "test_discover_page.py:616: UI interaction test - requires..."
                        if ": " in longrepr_str:
                            parts = longrepr_str.split(": ", 1)
                            if len(parts) >= 2:
                                # Get the second part (after "file:line: ")
                                potential_msg = parts[1]
                                # Split again in case there's another ": "
                                if ": " in potential_msg:
                                    msg_parts = potential_msg.split(": ", 1)
                                    skip_reason = msg_parts[-1].strip()
                                else:
                                    skip_reason = potential_msg.strip()
                        
                        # Clean up any remaining artifacts
                        if skip_reason:
                            # Remove trailing quotes, parentheses, brackets etc that pytest adds
                            skip_reason = skip_reason.rstrip("'\")])}")
                except Exception as e:
                    skip_reason = None
                
                # If still no reason, use default
                if not skip_reason:
                    skip_reason = "Test skipped"
            
            self.results.append({
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "duration": report.duration,
                "skip_reason": skip_reason
            })
            if report.outcome == "passed":
                self.passed += 1
            elif report.outcome == "failed":
                self.failed += 1
            elif report.outcome == "skipped":
                self.skipped += 1


def load_test_metadata_from_csv(csv_file):
    """Load test metadata from new_test_plan.csv file.
    
    Returns:
        - metadata: dict mapping test function names to their metadata
        - metadata_by_id: dict mapping test IDs to their metadata
        - sections: list of sections in order
    """
    metadata = {}
    metadata_by_id = {}
    sections = []
    current_section = None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if this is a section header (Test Function Name is '-', indicates section row)
                # Section rows have format: "SectionName,,-,-,-,-,-,-"
                if row['Test Function Name'].strip() == '-' and not row['Function'].strip() and row['Test ID'].strip():
                    current_section = row['Test ID'].strip()
                    if current_section not in sections:
                        sections.append(current_section)
                    continue
                
                # Skip rows with no test function name or placeholder '-'
                if not row['Test Function Name'] or row['Test Function Name'].strip() == '-':
                    continue
                
                test_func_name = row['Test Function Name'].strip()
                test_id = row['Test ID'].strip()
                
                entry = {
                    "id": test_id,
                    "section": current_section,
                    "function": row['Function'].strip(),
                    "partition": row['Partition'].strip(),
                    "inputs": row['Inputs'].strip(),
                    "expected": row['Expected Outputs'].strip(),
                    "description": row['Description'].strip(),
                    "valid": row['Valid/Invalid'].strip(),
                }
                
                # Index by function name (if available)
                if test_func_name != "-":
                    metadata[test_func_name] = entry
                
                # Index by test ID
                if test_id:
                    metadata_by_id[test_id] = {**entry, "func_name": test_func_name}
    except Exception as e:
        print(f"Warning: Could not load test metadata from CSV: {e}")
        import traceback
        traceback.print_exc()
    
    return metadata, metadata_by_id, sections


def run_all_tests_and_generate_report(test_range, test_page):
    """Run all tests and generate a comprehensive test report.
    
    Args:
        test_range: "q" (quick, skip selenium) or "f" (full)
        test_page: "." (all) or specific test file name
    """
    
    # Define paths
    test_dir = Path(__file__).parent
    project_root = test_dir.parent.parent
    reports_dir = test_dir / "test_reports"
    
    # Create test_reports directory if it doesn't exist
    reports_dir.mkdir(exist_ok=True)
    
    # Calculate next report ID by counting existing reports
    existing_reports = list(reports_dir.glob("*_test_report_*.txt"))
    report_id = len(existing_reports) + 1
    
    # Generate timestamped filename with report ID
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = reports_dir / f"{report_id:03d}_test_report_{timestamp}.txt"
    
    # Set up Python path to find app module
    sys.path.insert(0, str(project_root))
    os.chdir(str(project_root))
    
    # Create result collector plugin
    collector = ResultCollector()
    
    # Get test files to run
    skip_selenium = (test_range == 'q')
    tests_to_run = get_test_files_to_run(test_dir, test_page, skip_selenium)
    
    print(f"\n{'='*60}")
    print(f"Running tests in {'QUICK' if skip_selenium else 'FULL'} mode")
    print(f"Test page: {test_page if test_page != '.' else 'ALL'}")
    print(f"{'='*60}\n")
    
    # Run pytest programmatically and capture results
    pytest_args = [
        "-v",
        "--tb=short",
        "--color=no",
        "-ra"
    ] + tests_to_run
    
    # Run tests with result collection
    exit_code = pytest.main(pytest_args, plugins=[collector])
    
    # Generate detailed text report based on actual results
    generate_text_report(test_dir, report_file, exit_code, collector, test_range)


def generate_text_report(test_dir, report_file, exit_code, collector, test_range):
    """Generate a detailed text report from actual test results and CSV metadata.
    
    Args:
        test_dir: Path to test directory
        report_file: Path to output report file
        exit_code: Exit code from pytest
        collector: ResultCollector instance with test results
        test_range: "q" (quick) or "f" (full)
    """
    
    # Load test metadata from CSV file
    csv_file = test_dir / "new_test_plan.csv"
    test_metadata, metadata_by_id, sections = load_test_metadata_from_csv(csv_file)
    
    # Prepare report content
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("SNIP-SNAP AUTOMATED TEST REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Create mapping of test function to result for quick lookup
    result_map = {}
    test_file_map = {}  # Map test function to its test file
    for result in collector.results:
        parts = result["nodeid"].split("::")
        if len(parts) >= 3:
            test_func_name = parts[-1]
            test_file = parts[0]  # Path to test file
            result_map[test_func_name] = result
            test_file_map[test_func_name] = test_file
    
    # Map test files to sections
    file_to_section = {
        "test_welcome_page.py": "Welcome",
        "test_login_page.py": "Login",
        "test_signup_page.py": "Signup",
        "test_my_profile_page.py": "My Profile",
        "test_barber_dashboard_page.py": "Barber Dashboard",
        "test_barber_profile_page.py": "Barber Profile",
        "test_barbershop_page.py": "Barbershop",
        "test_interactive_map_page.py": "Interactive Map",
        "test_review_widget.py": "Review widget",
        "test_discover_page.py": "Discover",
        "test_navbar.py": "Navbar",
    }
    
    # Separate supporting tests (not in metadata) from planned tests
    supporting_tests = {}  # section -> list of test functions
    for test_func, test_file in test_file_map.items():
        if test_func not in test_metadata:
            # This is a supporting test
            section = None
            for file_name, sec in file_to_section.items():
                if file_name in test_file:
                    section = sec
                    break
            
            if section:
                if section not in supporting_tests:
                    supporting_tests[section] = []
                supporting_tests[section].append(test_func)
    
    # Determine which tests are Selenium (quick mode skips them)
    selenium_tests = set()
    for result in collector.results:
        if "test_interactive_map_page" in result["nodeid"]:
            selenium_tests.add(result["nodeid"])
    
    # Process tests organized by section
    test_count = 0
    for section in sections:
        section_tests = []
        
        # Collect all planned tests for this section
        for func_name, metadata in test_metadata.items():
            if metadata.get("section") == section:
                section_tests.append((func_name, metadata))
        
        # Sort tests by ID (convert to tuple for custom sorting)
        def sort_key(item):
            func_name, metadata = item
            test_id = metadata["id"]
            # Handle test IDs like "3-ext"
            if '-' in test_id:
                base_id, ext = test_id.split('-')
                try:
                    return (int(base_id), ext)
                except:
                    return (999, ext)
            else:
                try:
                    return (int(test_id), '')
                except:
                    return (999, test_id)
        
        section_tests.sort(key=sort_key)
        
        # Add section header
        if section_tests or section in supporting_tests:
            report_lines.append("=" * 80)
            report_lines.append(f"SECTION: {section}")
            report_lines.append("-" * 80)
            report_lines.append("")
            
            # Add supporting tests for this section
            if section in supporting_tests:
                report_lines.append("Supporting tests:")
                for test_func in supporting_tests[section]:
                    result = result_map.get(test_func)
                    if result:
                        status = "[PASS]" if result["outcome"] == "passed" else "[FAIL]"
                    else:
                        status = "[NOT RUN]"
                    report_lines.append(f"    - {test_func} {status}")
                report_lines.append("")
            
            # Add planned tests for this section
            for func_name, metadata in section_tests:
                
                # Get test result if available
                result = result_map.get(func_name)
                
                # Determine status
                if result:
                    if result["outcome"] == "passed":
                        status = "PASS [OK]"
                    elif result["outcome"] == "failed":
                        status = "FAIL [ERROR]"
                    elif result["outcome"] == "skipped":
                        skip_reason = result.get("skip_reason", "Unknown reason")
                        if skip_reason and isinstance(skip_reason, str) and len(skip_reason) > 0:
                            # Show the actual skip reason - allow full message
                            status = f"SKIP [DEFERRED: {skip_reason}]"
                        else:
                            status = "SKIP [DEFERRED]"
                    else:
                        status = "SKIP [NOT RUN]"
                    duration = result["duration"]
                else:
                    # Test was not run - determine why
                    skip_reason = "[NOT RUN]"
                    
                    if func_name == "-":
                        skip_reason = "[NO TEST IMPL]"
                    elif section == "Interactive Map":
                        skip_reason = "[SKIP SELENIUM]"
                    elif section in ["Welcome", "Login", "Signup", "My Profile", "Barber Dashboard", "Review widget"]:
                        # Check if this is a section known to be incomplete
                        skip_reason = "[NOT IMPLEMENTED]"
                    
                    status = f"SKIP {skip_reason}"
                    duration = 0
                
                report_lines.append(f"Test ID: {metadata['id']}")
                report_lines.append(f"  Function: {metadata['function']} | Test Function Name: {func_name} | Partition: {metadata['partition']}")
                report_lines.append(f"  Description: {metadata['description']}")
                report_lines.append(f"  Inputs: {metadata['inputs']}")
                report_lines.append(f"  Expected Outputs: {metadata['expected']}")
                report_lines.append(f"  Valid/Invalid: {metadata['valid']}")
                report_lines.append(f"  Status: {status} | Duration: {duration:.3f}s")
                report_lines.append("")
    
    # Add summary
    report_lines.append("=" * 80)
    report_lines.append("TEST SUMMARY")
    report_lines.append("=" * 80)
    
    # Get report name from file path (without path, just filename without extension)
    report_name = report_file.stem  # e.g., "081_test_report_2026-05-07_18-01-47"
    
    # Determine test type
    test_type = "quick" if test_range == "q" else "full"
    
    # Calculate durations
    total_duration = sum(result["duration"] for result in collector.results)
    total_tests = collector.passed + collector.failed + collector.skipped
    avg_duration = total_duration / total_tests if total_tests > 0 else 0
    
    # Format duration nicely (hours:minutes:seconds)
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = total_duration % 60
    if hours > 0:
        duration_str = f"{hours}h {minutes}m {seconds:.2f}s"
    elif minutes > 0:
        duration_str = f"{minutes}m {seconds:.2f}s"
    else:
        duration_str = f"{seconds:.2f}s"
    
    # Count supporting tests and planned tests
    supporting_count = sum(len(tests) for tests in supporting_tests.values())
    planned_count = len(test_metadata)
    success_rate = (collector.passed / (total_tests - collector.skipped) * 100) if (total_tests - collector.skipped) > 0 else 0
    
    # Display new format summary
    report_lines.append(f"Test Report Name: {report_name}")
    report_lines.append(f"Test Report Type: {test_type}")
    report_lines.append(f"Total Duration: {duration_str}")
    report_lines.append(f"Average Duration per Test: {avg_duration:.3f}s")
    report_lines.append("")
    report_lines.append(f"Supporting Tests: {supporting_count}")
    report_lines.append(f"Planned Tests: {planned_count}")
    report_lines.append(f"Total Tests Run: {total_tests}")
    report_lines.append(f"Passed: {collector.passed}")
    report_lines.append(f"Failed: {collector.failed}")
    report_lines.append(f"Skipped: {collector.skipped}")
    report_lines.append(f"Success Rate: {success_rate:.1f}% (of non-skipped tests)")
    report_lines.append("")
    report_lines.append(f"Exit Code: {exit_code}")
    if exit_code == 0:
        report_lines.append("Status: ALL TESTS PASSED [OK]")
    else:
        report_lines.append("Status: SOME TESTS FAILED [FAIL]")
    report_lines.append("=" * 80)
    
    # Write to file with UTF-8 encoding
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    
    # Also print to console
    print("\n".join(report_lines))
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    test_range, test_page = get_test_config()
    run_all_tests_and_generate_report(test_range, test_page)
