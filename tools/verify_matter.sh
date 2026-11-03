#!/usr/bin/env bash
# Build orchestration only: application behavior is compiled from LexLean.
set -euo pipefail
source /etc/profile.d/prismpm-sdk.sh
# This binary and its oracle inventory were built together from the pinned SDK.
prism_sdk=/usr/local/bin/prismpm
if ! "$prism_sdk" --project . --json build > matter-build.json; then
  cat matter-build.json
  exit 1
fi
matter_build=$(python3 -c 'import json; print(json.load(open("matter-build.json"))["build_id"])')
matter_artifact="$PWD/.prism/build/$matter_build"
cargo test --locked --offline --manifest-path tests/matter/Cargo.toml \
  --config "patch.crates-io.prism-legal-matter.path=\"$matter_artifact/cargo/package\"" \
  --config "patch.crates-io.prism-stdlib.path=\"$PWD/.toolchain/prismpm/stdlib/generated/package\""
ln -s /opt/prismpm/oracles/node_modules tests/matter/node_modules
node tests/matter/holistic_runtime.mjs "$matter_artifact/view/browser"
CHROMIUM_EXECUTABLE=/ms-playwright/chromium_headless_shell-cft-157.0.8099.0/chrome-headless-shell-linux64/chrome-headless-shell \
  node tests/matter/run_browser.mjs "$matter_artifact/view/browser"
if ! "$prism_sdk" --project . --json verify > matter-verification.json; then
  cat matter-verification.json
  exit 1
fi
python3 - "$matter_artifact" <<'PY'
import shutil, sys
from pathlib import Path
shutil.copytree(Path(sys.argv[1]) / 'view/browser', 'matter-site')
PY
