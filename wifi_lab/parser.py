import csv
from .models import AccessPoint, Station


def normalize_mac(value):
    return value.strip().upper()


def parse_airodump_csv(filename):
    access_points = []
    stations = []

    with open(filename, newline="", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.reader(f))

    section = None

    for row in rows:
        if not row:
            continue

        first = row[0].strip()

        if first == "BSSID":
            section = "ap"
            continue

        if first == "Station MAC":
            section = "station"
            continue

        if section == "ap" and len(row) >= 14:
            access_points.append(AccessPoint(
                bssid=normalize_mac(row[0]),
                channel=row[3].strip(),
                signal=row[8].strip(),
                essid=row[13].strip(),
            ))

        elif section == "station" and len(row) >= 6:
            stations.append(Station(
                mac=normalize_mac(row[0]),
                bssid=normalize_mac(row[5]),
                signal=row[3].strip(),
            ))

    return access_points, stations
