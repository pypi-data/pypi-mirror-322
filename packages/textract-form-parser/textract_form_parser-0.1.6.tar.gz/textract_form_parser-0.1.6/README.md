# Textract Form Parser

[![Build and Publish](https://github.com/yogeshvar/text-extractor/actions/workflows/publish.yml/badge.svg?branch=master)](https://github.com/yogeshvar/text-extractor/actions/workflows/publish.yml)
[![PyPI version](https://badge.fury.io/py/textract-form-parser.svg)](https://badge.fury.io/py/textract-form-parser)
[![Built with Cursor](https://img.shields.io/badge/Built%20with-Cursor-blue?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyLjg0MzggMTEuOTE0MUwxOC4zNiAxNy40MzA0QzE4LjY0NjggMTcuNzE3MSAxOC42NDY4IDE4LjE4MzQgMTguMzYgMTguNDcwMUMxOC4wNzMzIDE4Ljc1NjggMTcuNjA3IDE4Ljc1NjggMTcuMzIwMyAxOC40NzAxTDExLjgwNDEgMTIuOTUzOUw2LjI4NzgyIDE4LjQ3MDFDNi4wMDExMiAxOC43NTY4IDUuNTM0ODIgMTguNzU2OCA1LjI0ODEyIDE4LjQ3MDFDNSAxOC4yMjE5IDUgMTcuODI4MSA1LjI0ODEyIDE3LjU4QzUuMjQ4MTIgMTcuNTggNS4yNDgxMiAxNy41OCA1LjI0ODEyIDE3LjU4TDEwLjc2NDQgMTIuMDYzN0w1LjI0ODEyIDYuNTQ3NDRDNSA2LjI5OTMyIDUgNS45MDU1NiA1LjI0ODEyIDUuNjU3NDRDNS40OTYyNCA1LjQwOTMyIDUuODkgNS40MDkzMiA2LjEzODEyIDUuNjU3NDRDNS44OSA1LjQwOTMyIDYuMjg3ODIgNS44MDcxNCA2LjI4NzgyIDUuODA3MTRMMTEuODA0MSAxMS4zMjM0TDE3LjMyMDMgNS44MDcxNEMxNy42MDcgNS41MjA0NCAxOC4wNzMzIDUuNTIwNDQgMTguMzYgNS44MDcxNEMxOC42NDY4IDYuMDkzODQgMTguNjQ2OCA2LjU2MDE0IDE4LjM2IDYuODQ2ODRMMTIuODQzOCAxMS45MTQxWiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)](https://cursor.sh)

A Python library for parsing AWS Textract form output. This library helps process and analyze form data extracted by AWS Textract, generating structured outputs and reports.

## Features

- Parse AWS Textract JSON output
- Extract form fields and tables
- Generate HTML reports
- Create concise and verbose outputs
- Command-line interface
- Logging and debugging support

## Installation

```bash
pip install textract-form-parser
```

## Usage

### As a Library

```python
from textract_parser import analyze_document, generate_html_report, create_concise_results

# Load your Textract JSON
with open("notebook.json", "r") as f:
    textract_json = json.load(f)

# Analyze document
analysis_results = analyze_document(textract_json)

# Generate HTML report
generate_html_report(analysis_results, "report.html")

# Get concise results
concise_results = create_concise_results(analysis_results)
```

### Command Line Interface

```bash
# Basic usage
textract-parser input.json -o output

# With verbose logging
textract-parser input.json -o output -v
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yogeshvar/text-extractor.git
cd text-extractor
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

### Code Formatting

Format code using the provided script:
```bash
./scripts/format.sh
```

This will:
- Fix end of files
- Fix trailing whitespace
- Run Black formatter
- Sort imports with isort
- Stage formatted files

### Testing

Run tests with coverage:
```bash
pytest --cov=textract_parser \
      --cov-report=term-missing \
      --html=test-results/report.html \
      --self-contained-html \
      -v
```

### Commit Guidelines

We use conventional commits. Format:
```
<type>: <description>

[optional body]
[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `enhance`: Enhancement
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### Release Process

1. Create a PR from your feature branch to master
2. Ensure all tests pass
3. Update version in:
   - `setup.py`
   - `textract_parser/__init__.py`
   - `pyproject.toml`
4. Merge PR to master
5. GitHub Actions will automatically:
   - Run tests
   - Create a new tag
   - Generate release notes
   - Create GitHub release
   - Publish to PyPI

## License

MIT License - see [LICENSE](LICENSE) for details

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Format code (`./scripts/format.sh`)
4. Commit changes (`git commit -m 'feat: add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Authors

- Yogeshvar Senthilkumar - [yogeshvar@icloud.com](mailto:yogeshvar@icloud.com)
