#!/usr/bin/env bash
# Build the bilingual (EN/FA) aiorubi documentation.
# Usage: bash scripts/build-docs-bilingual.sh [docs_dir] [out_dir]
set -euo pipefail

DOCS_DIR="${1:-docs}"
OUT_DIR="${2:-_build/html}"

cd "$(dirname "$0")/.."            # repo root
cd "$DOCS_DIR"

echo "==> Clean bilingual output"
rm -rf "$OUT_DIR/en" "$OUT_DIR/fa"

echo "==> English build"
sphinx-build -b html . "$OUT_DIR/en"

echo "==> Persian (RTL) build"
sphinx-build -b html -D language=fa . "$OUT_DIR/fa"

echo "==> Done: $OUT_DIR/en  +  $OUT_DIR/fa"
