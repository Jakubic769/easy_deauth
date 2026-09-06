import json
from pathlib import Path

def normalize_mac(value: str) -> str:
    return value.strip().upper().replace("-", ":")

class LabConfig:
    def __init__(self, filename="config.json"):
        with Path(filename).open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.allowed_bssids = {normalize_mac(x) for x in data.get("allowed_bssids", [])}

    def is_allowed_ap(self, ap) -> bool:
        return normalize_mac(ap.bssid) in self.allowed_bssids

    def is_allowed_station(self, station, ap) -> bool:
        return self.is_allowed_ap(ap) and normalize_mac(station.bssid) == normalize_mac(ap.bssid)
