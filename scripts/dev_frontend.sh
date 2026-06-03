#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/front/cloud_agent"

export VITE_API_BASE_URL="${VITE_API_BASE_URL:-http://127.0.0.1:5001}"
exec node node_modules/vite/bin/vite.js --host 127.0.0.1 --port "${FRONTEND_PORT:-5174}"

