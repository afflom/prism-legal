#!/usr/bin/env bash
set -euo pipefail
# api check already includes sanitization and the legacy model/fixture checks.
./bin/prism-legal api check
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/ci/*.test.cjs
