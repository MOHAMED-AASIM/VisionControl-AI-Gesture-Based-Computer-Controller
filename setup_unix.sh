#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"

case "$PWD" in
    *[! -~]*) echo "ERROR: move this project to an ASCII-only path: $PWD" >&2; exit 1 ;;
esac

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
echo "Setup complete. Run: .venv/bin/python main.py"