#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Prefer an existing project venv, fall back to .venv inside the repo.
if [[ -d "$SCRIPT_DIR/.hack_venv" ]]; then
  VENV_DIR="$SCRIPT_DIR/.hack_venv"
else
  VENV_DIR="$SCRIPT_DIR/.venv"
  if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
  fi
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

if [[ -x "$VENV_DIR/bin/python3" ]]; then
  PYTHON_BIN="$VENV_DIR/bin/python3"
elif [[ -x "$VENV_DIR/bin/python" ]]; then
  PYTHON_BIN="$VENV_DIR/bin/python"
else
  echo "Could not locate python interpreter in $VENV_DIR/bin" >&2
  exit 1
fi

"$PYTHON_BIN" -m pip install --upgrade pip >/dev/null
"$PYTHON_BIN" -m pip install -r backend/requirements.txt

exec "$PYTHON_BIN" backend/main.py
