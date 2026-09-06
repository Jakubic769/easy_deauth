from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt
from rich.table import Table

from wifi_lab.interfaces import list_wifi_interfaces, enable_monitor_mode, restore_managed_mode
from wifi_lab.scanner import scan
from wifi_lab.parser import parse_airodump_csv
from wifi_lab.lab import LabConfig
from wifi_lab.vendor import lookup_vendor

console = Console()

def choose(items, title, label):
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("Value")
    for i, item in enumerate(items, 1):
        table.add_row(str(i), str(item))
    console.print(table)
    return items[IntPrompt.ask(label, choices=[str(i) for i in range(1, len(items)+1)]) - 1]

def show_aps(aps):
    table = Table(title="Detected access points")
    for c in ("#", "BSSID", "CH", "Signal", "ESSID"):
        table.add_column(c)
    for i, ap in enumerate(aps, 1):
        table.add_row(str(i), ap.bssid, ap.channel, ap.signal, ap.essid or "<hidden>")
    console.print(table)

def show_stations(stations):
    table = Table(title="Stations associated with selected AP")
    for c in ("#", "MAC Address", "Vendor", "BSSID", "Signal"):
        table.add_column(c)
    for i, station in enumerate(stations, 1):
        table.add_row(
            str(i), station.mac, lookup_vendor(station.mac),
            station.bssid, station.signal
        )
    console.print(table)

def main():
    console.print(Panel.fit(
        "[bold cyan]Easy WiFi Lab[/bold cyan]\n[dim]Authorized wireless laboratory scanner[/dim]",
        border_style="cyan",
    ))

    lab = LabConfig()
    monitor = None

    try:
        interfaces = list_wifi_interfaces()
        if not interfaces:
            console.print("[red]No Wi-Fi interfaces were found.[/red]")
            return

        interface = choose(interfaces, "Wi-Fi interfaces", "Select an interface")

        if not Confirm.ask(f"Switch [bold]{interface}[/bold] to monitor mode?"):
            return

        monitor = enable_monitor_mode(interface)
        console.print(f"[green]Monitor mode enabled:[/green] {monitor}")
        console.print("[yellow]Scanning passively for 15 seconds...[/yellow]")

        csv_file = scan(monitor, seconds=15)
        aps, stations = parse_airodump_csv(csv_file)

        if not aps:
            console.print("[yellow]No access points were detected.[/yellow]")
            return

        show_aps(aps)
        selected_ap = choose(aps, "Detected access points", "Select your AP")

        target_stations = [
            s for s in stations
            if s.bssid.strip().upper().replace("-", ":")
            == selected_ap.bssid.strip().upper().replace("-", ":")
        ]

        if not target_stations:
            console.print("[yellow]No stations were detected for this AP.[/yellow]")
            return

        show_stations(target_stations)
        selected_station = choose(target_stations, "Detected stations", "Select a station")

        # Fixed validation: normalize MAC/BSSID formatting and validate
        # the AP allow-list separately from the station association.
        if not lab.is_allowed_ap(selected_ap):
            console.print(Panel(
                "The selected AP is not listed in config.json::allowed_bssids.",
                title="Lab validation failed",
                border_style="red",
            ))
            return

        if not lab.is_allowed_station(selected_station, selected_ap):
            console.print(Panel(
                "The selected station is not associated with the selected AP.",
                title="Station validation failed",
                border_style="red",
            ))
            return

        console.print(Panel(
            f"[bold green]TARGET VALIDATED[/bold green]\n\n"
            f"AP BSSID: {selected_ap.bssid}\n"
            f"ESSID: {selected_ap.essid or '<hidden>'}\n"
            f"Channel: {selected_ap.channel}\n\n"
            f"Station MAC: {selected_station.mac}\n"
            f"Vendor: {lookup_vendor(selected_station.mac)}\n"
            f"Signal: {selected_station.signal}",
            border_style="green",
        ))
        console.print("[dim]Active deauthentication is intentionally not automated in this build.[/dim]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
    except Exception as exc:
        console.print(f"[red]Error: {exc}[/red]")
    finally:
        if monitor:
            try:
                restore_managed_mode(monitor)
                console.print("[green]Interface restored to managed mode.[/green]")
            except Exception as exc:
                console.print(f"[yellow]Could not restore interface: {exc}[/yellow]")

if __name__ == "__main__":
    main()
