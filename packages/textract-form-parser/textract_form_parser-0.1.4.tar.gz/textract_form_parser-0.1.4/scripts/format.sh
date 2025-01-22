#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting format fixes...${NC}"

# Fix end of files
echo -e "\n${BLUE}Fixing end of files...${NC}"
pre-commit run end-of-file-fixer --all-files

# Fix trailing whitespace
echo -e "\n${BLUE}Fixing trailing whitespace...${NC}"
pre-commit run trailing-whitespace --all-files

# Format Python files using black
echo -e "\n${BLUE}Running Black formatter...${NC}"
pre-commit run black --all-files

# Sort imports using isort
echo -e "\n${BLUE}Sorting imports with isort...${NC}"
pre-commit run isort --all-files

# Stage the formatted files
echo -e "\n${BLUE}Staging formatted files...${NC}"
git add $(git diff --name-only)

echo -e "\n${GREEN}Formatting complete! ✨${NC}"
