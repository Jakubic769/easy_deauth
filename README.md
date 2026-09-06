# Easy WiFi Lab

> Passive Wi-Fi discovery CLI for authorized security labs and your own equipment.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Linux](https://img.shields.io/badge/Linux-iw%20%2B%20Aircrack--ng-black?logo=linux)
![Status](https://img.shields.io/badge/Status-Lab%20Tool-success)

## Features

- 📡 Wireless adapter discovery
- 👀 Monitor-mode capture
- ⏱️ 15-second passive scan
- 📶 AP selection
- 🖥️ Station discovery per BSSID
- 🏷️ Best-effort MAC/OUI vendor lookup
- ✅ Station ↔ BSSID validation
- 🔄 Automatic managed-mode restore
- 🧩 No `config.json` / no whitelist layer

## Flow

```text
Adapter → Monitor Mode → Passive Scan → AP → Stations → Validate → Exit
```

## Install

### Linux / WSL

```bash
chmod +x install_easy_deauth.sh
./install_easy_deauth.sh
```

Then:

```bash
easy_deauth
```

### Windows

The `.bat` files are WSL launchers. Linux wireless tooling must run inside a suitable Linux environment with a compatible Wi-Fi adapter.

## Requirements

- Python 3.10+
- `iw`
- Aircrack-ng / `airodump-ng`
- Wi-Fi adapter supporting monitor mode
- `sudo`

## Structure

```text
main.py
wifi_lab/
├── interfaces.py
├── scanner.py
├── parser.py
├── models.py
└── vendor.py
```

## Safety

Use only on networks and devices you own or are explicitly authorized to test.

The project focuses on passive discovery and target validation; it does not automate active packet-disruption/deauthentication.

## License

Choose and add a license appropriate for your repository.
