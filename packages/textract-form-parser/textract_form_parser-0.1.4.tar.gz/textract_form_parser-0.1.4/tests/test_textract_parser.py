import json
import os

import pytest

from textract_parser import (
    analyze_document,
    create_concise_results,
    generate_html_report,
    setup_textract_logger,
)


@pytest.fixture
def sample_json():
    """Load sample Textract JSON"""
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "notebook.json")
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def output_dir(tmp_path):
    """Create temporary output directory"""
    return tmp_path / "test_output"


def test_complete_workflow(sample_json, output_dir):
    """Test complete workflow including all output files"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Setup logger
    logger = setup_textract_logger(verbose=True, log_dir=str(output_dir))

    # Analyze document
    analysis_results = analyze_document(sample_json)

    # Generate all outputs
    report_file = output_dir / "textract_report.html"
    verbose_json = output_dir / "analysis_results_verbose.json"
    concise_json = output_dir / "analysis_results_concise.json"
    log_file = output_dir / "textract.log"

    # Generate HTML report
    generate_html_report(analysis_results, str(report_file))

    # Save verbose JSON
    with open(verbose_json, "w") as f:
        json.dump(analysis_results, f, indent=2)

    # Create and save concise results
    concise_results = create_concise_results(analysis_results)
    with open(concise_json, "w") as f:
        json.dump(concise_results, f, indent=2)

    # Verify all files were created
    assert report_file.exists(), "HTML report not created"
    assert verbose_json.exists(), "Verbose JSON not created"
    assert concise_json.exists(), "Concise JSON not created"
    assert log_file.exists(), "Log file not created"

    # Verify file contents
    assert report_file.stat().st_size > 0, "HTML report is empty"
    assert verbose_json.stat().st_size > 0, "Verbose JSON is empty"
    assert concise_json.stat().st_size > 0, "Concise JSON is empty"
    assert log_file.stat().st_size > 0, "Log file is empty"

    # Verify JSON structure
    with open(verbose_json) as f:
        verbose_data = json.load(f)
        assert "layout" in verbose_data
        assert "form_fields" in verbose_data

    with open(concise_json) as f:
        concise_data = json.load(f)
        assert "layout" in concise_data
        assert "form_fields" in concise_data
