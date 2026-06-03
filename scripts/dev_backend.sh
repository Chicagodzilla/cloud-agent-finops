#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/app"

export MOCK_DATA_MODE="${MOCK_DATA_MODE:-true}"
exec ../.venv/bin/python -m uvicorn app_main:app --host 0.0.0.0 --port "${BACKEND_PORT:-5001}" --reload

