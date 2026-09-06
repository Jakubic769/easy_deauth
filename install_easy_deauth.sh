#!/usr/bin/env bash
set -e

PROJECT_DIR="$HOME/easy_deauth"

echo "[1/4] Checking Linux dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip iw aircrack-ng

echo "[2/4] Installing project..."
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cp -r ./* "$PROJECT_DIR/"

echo "[3/4] Creating virtual environment..."
python3 -m venv "$PROJECT_DIR/.venv"
"$PROJECT_DIR/.venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

echo "[4/4] Installing command..."
sudo tee /usr/local/bin/easy_deauth >/dev/null <<EOF
#!/usr/bin/env bash
cd "$PROJECT_DIR"
exec sudo "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/main.py" "\$@"
EOF
sudo chmod +x /usr/local/bin/easy_deauth

echo
echo "Installation complete."
echo "Run: easy_deauth"
