import json
from pathlib import Path


class LabConfig:
    def __init__(self, filename="config.json"):
        with Path(filename).open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.allowed_bssids = {
            mac.strip().upper()
            for mac in data.get("allowed_bssids", [])
        }

    def is_allowed_ap(self, ap):
        return ap.bssid.upper() in self.allowed_bssids

    def is_allowed_station(self, station, ap):
        return (
            self.is_allowed_ap(ap)
            and station.bssid.upper() == ap.bssid.upper()
        )
