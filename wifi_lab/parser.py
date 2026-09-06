from __future__ import annotations

import csv
from pathlib import Path

from .models import AccessPoint, Station


def _clean(value: str) -> str:
    return value.strip()


def parse_scan(path: Path):
    aps: list[AccessPoint] = []
    stations: list[Station] = []

    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        rows = list(csv.reader(fh))

    ap_header = next(
        (i for i, row in enumerate(rows) if row and row[0].strip() == "BSSID"),
        None,
    )
    station_header = next(
        (i for i, row in enumerate(rows) if row and row[0].strip() == "Station MAC"),
        None,
    )

    if ap_header is not None:
        for row in rows[ap_header + 1: station_header if station_header is not None else len(rows)]:
            if len(row) < 14 or not row[0].strip():
                continue
            aps.append(
                AccessPoint(
                    bssid=_clean(row[0]),
                    channel=_clean(row[3]),
                    signal=_clean(row[8]),
                    essid=_clean(row[13]),
                )
            )

    if station_header is not None:
        for row in rows[station_header + 1:]:
            if len(row) < 6 or not row[0].strip():
                continue
            stations.append(
                Station(
                    mac=_clean(row[0]),
                    signal=_clean(row[3]),
                    bssid=_clean(row[5]),
                )
            )

    return aps, stations
