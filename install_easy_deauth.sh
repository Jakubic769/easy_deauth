#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_NAME="easy_deauth"
PROJECT_DIR="$HOME/$PROJECT_NAME"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "        Easy WiFi Lab Installer"
echo "=========================================="
echo

# ------------------------------------------
# Check operating system
# ------------------------------------------

if [[ ! -f /etc/os-release ]]; then
    echo "[ERROR] /etc/os-release was not found."
    echo "This installer currently supports Debian-based Linux systems."
    exit 1
fi

source /etc/os-release

case "${ID:-}" in
    debian|ubuntu|kali|linuxmint|pop)
        ;;
    *)
        echo "[ERROR] Unsupported distribution: ${PRETTY_NAME:-unknown}"
        echo "Supported: Debian, Ubuntu, Kali, Linux Mint and Pop!_OS."
        exit 1
        ;;
esac

# ------------------------------------------
# Check sudo
# ------------------------------------------

if ! command -v sudo >/dev/null 2>&1; then
    echo "[ERROR] sudo is not installed."
    exit 1
fi

if ! sudo -v; then
    echo "[ERROR] sudo authentication failed."
    exit 1
fi

# ------------------------------------------
# Check required project files
# ------------------------------------------

if [[ ! -f "$SCRIPT_DIR/main.py" ]]; then
    echo "[ERROR] main.py was not found."
    echo
    echo "Run this installer from the project directory:"
    echo "  cd /path/to/easy_deauth"
    echo "  ./install_easy_deauth.sh"
    exit 1
fi

if [[ ! -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo "[ERROR] requirements.txt was not found."
    exit 1
fi

if [[ ! -d "$SCRIPT_DIR/wifi_lab" ]]; then
    echo "[ERROR] wifi_lab directory was not found."
    exit 1
fi

# ------------------------------------------
# Install system dependencies
# ------------------------------------------

echo "[1/5] Installing Linux dependencies..."

sudo apt-get update

sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    iw \
    aircrack-ng

# ------------------------------------------
# Install project
# ------------------------------------------

echo "[2/5] Installing project into:"
echo "      $PROJECT_DIR"

if [[ "$SCRIPT_DIR" != "$PROJECT_DIR" ]]; then
    rm -rf "$PROJECT_DIR"
    mkdir -p "$PROJECT_DIR"

    cp -a "$SCRIPT_DIR/." "$PROJECT_DIR/"
fi

# ------------------------------------------
# Create virtual environment
# ------------------------------------------

echo "[3/5] Creating Python virtual environment..."

python3 -m venv "$PROJECT_DIR/.venv"

"$PROJECT_DIR/.venv/bin/python" -m pip install --upgrade pip

"$PROJECT_DIR/.venv/bin/python" -m pip install \
    -r "$PROJECT_DIR/requirements.txt"

# ------------------------------------------
# Install global command
# ------------------------------------------

echo "[4/5] Installing 'easy_deauth' command..."

sudo tee "/usr/local/bin/easy_deauth" >/dev/null <<EOF
#!/usr/bin/env bash

cd "$PROJECT_DIR"
exec sudo "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/main.py" "\$@"
EOF

sudo chmod +x "/usr/local/bin/easy_deauth"

# ------------------------------------------
# Verify installation
# ------------------------------------------

echo "[5/5] Verifying installation..."

if ! command -v iw >/dev/null 2>&1; then
    echo "[ERROR] iw installation failed."
    exit 1
fi

if ! command -v airodump-ng >/dev/null 2>&1; then
    echo "[ERROR] aircrack-ng installation failed."
    exit 1
fi

if [[ ! -x "$PROJECT_DIR/.venv/bin/python" ]]; then
    echo "[ERROR] Python virtual environment was not created."
    exit 1
fi

if [[ ! -x "/usr/local/bin/easy_deauth" ]]; then
    echo "[ERROR] easy_deauth command was not installed."
    exit 1
fi

echo
echo "=========================================="
echo "       Installation complete!"
echo "=========================================="
echo
echo "Project:"
echo "  $PROJECT_DIR"
echo
echo "Run the program with:"
echo
echo "  easy_deauth"
echo
echo "Check the command with:"
echo
echo "  command -v easy_deauth"
echo
echo "=========================================="