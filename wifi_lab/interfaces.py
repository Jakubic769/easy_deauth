from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class WirelessInterface:
    name: str
    mode: str


def list_wireless_interfaces() -> list[WirelessInterface]:
    result = subprocess.run(
        ["iw", "dev"],
        capture_output=True,
        text=True,
        check=True,
    )

    interfaces: list[WirelessInterface] = []
    current: WirelessInterface | None = None

    for raw in result.stdout.splitlines():
        line = raw.strip()

        if line.startswith("Interface "):
            current = WirelessInterface(line.split(None, 1)[1], "unknown")
            interfaces.append(current)
        elif current and line.startswith("type "):
            current.mode = line.split(None, 1)[1]

    return interfaces


def _run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def set_monitor_mode(interface: str) -> str:
    _run("sudo", "ip", "link", "set", interface, "down")
    _run("sudo", "iw", "dev", interface, "set", "type", "monitor")
    _run("sudo", "ip", "link", "set", interface, "up")
    return interface


def set_managed_mode(interface: str) -> None:
    _run("sudo", "ip", "link", "set", interface, "down")
    _run("sudo", "iw", "dev", interface, "set", "type", "managed")
    _run("sudo", "ip", "link", "set", interface, "up")
