from urllib.request import Request, urlopen
import re

def normalize_mac(mac):
    return re.sub(r"[^0-9A-Fa-f]", "", mac).upper()

def lookup_vendor(mac):
    value = normalize_mac(mac)
    if len(value) < 6:
        return "Unknown"
    try:
        req = Request(
            f"https://api.macvendors.com/{value[:6]}",
            headers={"User-Agent": "EasyWiFiLab/1.0"},
        )
        with urlopen(req, timeout=3) as response:
            result = response.read().decode("utf-8", errors="replace").strip()
        return result or "Unknown"
    except Exception:
        return "Unknown"
