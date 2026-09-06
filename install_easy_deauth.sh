#!/usr/bin/env bash
set -euo pipefail
APP="Easy WiFi Lab"
INSTALL_DIR="${HOME}/easy_deauth"
VENV="${INSTALL_DIR}/.venv"
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

B="\033[1m"; C="\033[36m"; G="\033[32m"; Y="\033[33m"; R="\033[31m"; D="\033[90m"; X="\033[0m"
ok(){ printf "  ${G}✔${X} %s\n" "$1"; }
info(){ printf "  ${C}●${X} %s\n" "$1"; }
warn(){ printf "  ${Y}!${X} %s\n" "$1"; }
die(){ printf "  ${R}✖${X} %s\n" "$1"; exit 1; }

clear 2>/dev/null || true
printf "\n${C}${B}"
cat <<'EOF'
   ███████╗ █████╗ ███████╗██╗   ██╗
   ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝
   █████╗  ███████║███████╗ ╚████╔╝
   ██╔══╝  ██╔══██║╚════██║  ╚██╔╝
   ██║     ██║  ██║███████║   ██║
   ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝
EOF
printf "${X}   ${B}${APP}${X} ${D}• installer${X}\n"
printf "   ${D}────────────────────────────────────────────────────────────${X}\n\n"

[[ $EUID -ne 0 ]] || die "Run as a normal user, not root."
command -v sudo >/dev/null || die "sudo is required."
[[ -f /etc/os-release ]] || die "Linux distribution not detected."
source /etc/os-release
info "Detected ${PRETTY_NAME:-Linux}"

case "${ID:-}" in
  debian|ubuntu|kali|linuxmint|pop)
    info "Installing system dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -y python3 python3-venv python3-pip iw aircrack-ng >/dev/null
    ok "System dependencies ready"
    ;;
  *)
    warn "Unsupported distro. Make sure python3, venv, iw and aircrack-ng are installed."
    ;;
esac

[[ -f "$HERE/main.py" ]] || die "main.py not found."
[[ -d "$HERE/wifi_lab" ]] || die "wifi_lab/ not found."
[[ -f "$HERE/requirements.txt" ]] || die "requirements.txt not found."

info "Installing project to $INSTALL_DIR"
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -a "$HERE/main.py" "$HERE/wifi_lab" "$HERE/requirements.txt" "$INSTALL_DIR/"
[[ -f "$HERE/README.md" ]] && cp -a "$HERE/README.md" "$INSTALL_DIR/"
ok "Project files copied"

info "Creating Python virtual environment..."
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip -q
"$VENV/bin/pip" install -r "$INSTALL_DIR/requirements.txt" -q
ok "Python environment ready"

info "Installing launcher..."
sudo tee /usr/local/bin/easy_deauth >/dev/null <<EOF
#!/usr/bin/env bash
exec "$VENV/bin/python" "$INSTALL_DIR/main.py" "\$@"
EOF
sudo chmod +x /usr/local/bin/easy_deauth
ok "Launcher available as: easy_deauth"

printf "\n   ${G}${B}Installation complete.${X}\n"
printf "   ${D}Run:${X} ${C}easy_deauth${X}\n\n"
