#!/bin/bash

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only)

if [ -z "$STAGED_FILES" ]; then
    echo "No files staged for commit"
    exit 0
fi

# Run pre-commit only on staged files
echo "Running pre-commit on staged files..."
pre-commit run --files $STAGED_FILES

exit $?
