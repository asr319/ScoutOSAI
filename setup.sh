#!/bin/bash
set -e

# Determine the repository root based on the script location
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Ensure pnpm is available
corepack enable pnpm

# Install backend dependencies (including development requirements)
cd "$REPO_ROOT/bekonos-backend"
pip install -r requirements.txt -r requirements-dev.txt

# Install frontend dependencies
cd "$REPO_ROOT/bekonos-frontend"
pnpm install

# Return to the repository root when finished
cd "$REPO_ROOT"


