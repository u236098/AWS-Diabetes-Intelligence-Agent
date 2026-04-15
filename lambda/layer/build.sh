#!/bin/bash
# Build Lambda Layer with dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYER_DIR="${SCRIPT_DIR}/python"

echo "Building Lambda Layer..."

# Clean previous build
rm -rf "${LAYER_DIR}"
mkdir -p "${LAYER_DIR}"

# Install dependencies
pip install -r "${SCRIPT_DIR}/requirements.txt" -t "${LAYER_DIR}" --upgrade

echo "Lambda Layer built successfully at: ${LAYER_DIR}"
