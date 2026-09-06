from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def scan(interface: str, duration: int = 15) -> Path:
    """Run a passive airodump-ng CSV capture and return its CSV path."""
    tmp = Path(tempfile.mkdtemp(prefix="easy_wifi_lab_"))
    prefix = tmp / "scan"

    try:
        subprocess.run(
            [
                "sudo",
                "timeout",
                str(duration),
                "airodump-ng",
                "--write-interval",
                "1",
                "--output-format",
                "csv",
                "--write",
                str(prefix),
                interface,
            ],
            check=False,
        )

        csv_path = Path(str(prefix) + "-01.csv")
        if not csv_path.exists():
            raise RuntimeError(
                "airodump-ng did not produce a CSV file. "
                "Check that the adapter is in monitor mode and supports capture."
            )

        # Keep the result available to the parser after this function returns.
        persistent = Path.cwd() / ".easy_wifi_lab_scan.csv"
        persistent.write_bytes(csv_path.read_bytes())
        return persistent
    finally:
        shutil = __import__("shutil")
        shutil.rmtree(tmp, ignore_errors=True)
