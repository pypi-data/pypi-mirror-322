"""
Command-line interface for Textract Form Parser
"""

import argparse
import json
import os
import sys
from datetime import datetime

from textract_parser import (
    analyze_document,
    create_concise_results,
    generate_html_report,
    setup_textract_logger,
)


def create_parser():
    parser = argparse.ArgumentParser(
        description="Parse AWS Textract form output and generate reports"
    )
    parser.add_argument(
        "input_file",
        help="Input JSON file containing Textract output",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output",
        help="Output directory for reports (default: output)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


def _create_timestamped_dir() -> str:
    """
    Create a timestamped directory for storing analysis outputs.

    This function:
    1. Generates a timestamp in human-readable format
    2. Creates a directory using the timestamp
    3. Ensures the directory exists

    Directory Format:
        logs/MMM_DD_YYYY_HHMM (e.g., logs/Jan_19_2025_1000)

    Returns:
        str: Path to the created directory

    Note:
        - Uses exist_ok=True to handle concurrent directory creation
        - Month is abbreviated to three letters
        - Time is in 24-hour format

    Example:
        >>> dir_path = _create_timestamped_dir()
        >>> print(dir_path)
        'logs/Jan_19_2025_1000'
    """
    timestamp = datetime.now().strftime("%b_%d_%Y_%H%M")
    log_dir = os.path.join("logs", timestamp)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    return log_dir


def main():
    """
    Main function to process AWS Textract JSON output and generate analysis reports.

    Workflow:
    1. Creates timestamped output directory
    2. Initializes logging system
    3. Reads Textract JSON input
    4. Processes document and extracts information
    5. Generates three types of output:
       - HTML report: Visual representation with details
       - Verbose JSON: Complete analysis data
       - Concise JSON: Simplified essential information

    Directory Structure:
    logs/
    └── Jan_19_2025_1000/
        ├── textract_report.html    # Detailed visual report
        ├── analysis_results_verbose.json  # Complete data
        ├── analysis_results_concise.json  # Essential data
        └── textract.log           # Processing log

    Input:
        Expects 'notebook.json' in the current directory

    Raises:
        FileNotFoundError: If notebook.json is missing
        json.JSONDecodeError: If JSON is malformed
        Exception: For other processing errors

    Note:
        All outputs are organized in a timestamped directory
        for easy tracking and management
    """
    try:
        # Create output directory and setup logging
        log_dir = _create_timestamped_dir()
        logger = setup_textract_logger(verbose=False, log_dir=log_dir)

        # Read and analyze input
        with open("notebook.json", "r") as f:
            textract_json = json.load(f)
        analysis_results = analyze_document(textract_json)

        # Setup output paths
        report_file = os.path.join(log_dir, "textract_report.html")
        verbose_json = os.path.join(log_dir, "analysis_results_verbose.json")
        concise_json = os.path.join(log_dir, "analysis_results_concise.json")

        # Generate outputs
        generate_html_report(analysis_results, report_file)

        with open(verbose_json, "w") as f:
            json.dump(analysis_results, f, indent=2)

        concise_results = create_concise_results(analysis_results)
        with open(concise_json, "w") as f:
            json.dump(concise_results, f, indent=2)

        # Log completion
        logger.info(f"Analysis complete. Check the reports in: {log_dir}")
        logger.info(f"Full HTML Report: {report_file}")
        logger.info(f"Verbose JSON: {verbose_json}")
        logger.info(f"Concise JSON: {concise_json}")

    except FileNotFoundError:
        logger.error("Could not find the JSON file")
    except json.JSONDecodeError:
        logger.error("Invalid JSON file")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    sys.exit(main())
