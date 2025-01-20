#!/bin/bash

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit separately first
pip install pre-commit

# Install the package in editable mode
pip install -e .

# Install pre-commit hooks
pre-commit install -t pre-commit
pre-commit install -t commit-msg

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
fi

# Set up custom pre-commit hook
PRE_COMMIT_SCRIPT=".git/hooks/pre-commit"
echo '#!/bin/bash' > "$PRE_COMMIT_SCRIPT"
echo './scripts/pre-commit-staged.sh' >> "$PRE_COMMIT_SCRIPT"
chmod +x "$PRE_COMMIT_SCRIPT"

echo "Setup complete! Commit hooks are now installed."
