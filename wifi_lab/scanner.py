import subprocess
import tempfile
from pathlib import Path


def scan(interface, seconds=15):
    temp_dir = Path(tempfile.mkdtemp(prefix="easy-wifi-lab-"))
    prefix = temp_dir / "scan"

    command = [
        "sudo", "timeout", str(seconds),
        "airodump-ng",
        "--write", str(prefix),
        "--output-format", "csv",
        interface,
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    matches = sorted(temp_dir.glob("scan*.csv"))
    if not matches:
        raise RuntimeError("airodump-ng did not produce a CSV file.")

    return matches[0]
