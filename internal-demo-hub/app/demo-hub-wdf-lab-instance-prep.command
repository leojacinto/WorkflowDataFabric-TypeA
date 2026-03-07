#!/bin/bash
# ============================================================
# Demo Hub WDF Lab Instance Prep — Mac/Linux Launcher
# ============================================================
# This script checks for Python 3, installs dependencies,
# and launches the web UI in your browser.
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
APP="$SCRIPT_DIR/demo_hub_prep.py"

echo ""
echo "  ================================================"
echo "  Demo Hub WDF Lab — Instance Prep"
echo "  ================================================"
echo ""

# --- Check Python 3 ---
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PY_VER=$(python --version 2>&1)
    if echo "$PY_VER" | grep -q "Python 3"; then
        PYTHON="python"
    fi
fi

if [ -z "$PYTHON" ]; then
    echo "  Python 3 is not installed."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Installing Python 3 via Homebrew..."
        if ! command -v brew &>/dev/null; then
            echo "  Homebrew not found. Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3
        PYTHON="python3"
    else
        echo "  Please install Python 3:"
        echo "    Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
        echo "    Fedora:        sudo dnf install python3"
        echo ""
        exit 1
    fi
fi

echo "  Using: $($PYTHON --version)"

# --- Create virtual environment if needed ---
if [ ! -d "$VENV_DIR" ]; then
    echo "  Setting up environment (first run only)..."
    $PYTHON -m venv "$VENV_DIR"
fi

# --- Activate venv and install dependencies ---
source "$VENV_DIR/bin/activate"
pip install -q --upgrade pip 2>/dev/null
pip install -q -r "$REQUIREMENTS" 2>/dev/null
echo "  Dependencies ready."
echo ""

# --- Run the app ---
python "$APP"
