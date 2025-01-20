"""
Textract Form Parser
A Python library for parsing AWS Textract form output
"""

from textract_parser.textract_parser import (
    analyze_document,
    create_concise_results,
    generate_html_report,
    setup_textract_logger,
)

__version__ = "0.1.3"
__author__ = "Yogeshvar Senthilkumar"
__email__ = "yogeshvar@icloud.com"

__all__ = [
    "analyze_document",
    "create_concise_results",
    "generate_html_report",
    "setup_textract_logger",
]
