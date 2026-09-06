from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.prompt import Confirm, IntPrompt
from rich.table import Table

from wifi_lab.interfaces import list_wifi_interfaces, enable_monitor_mode, restore_managed_mode
from wifi_lab.scanner import scan
from wifi_lab.parser import parse_airodump_csv
from wifi_lab.lab import LabConfig

console = Console()


def banner():
    console.print(Panel.fit(
        "[bold cyan]Easy WiFi Lab[/bold cyan]\n"
        "[dim]Authorized passive wireless lab scanner[/dim]",
        border_style="cyan",
    ))


def choose(items, title, label):
    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("Value")
    for i, item in enumerate(items, 1):
        table.add_row(str(i), str(item))
    console.print(table)
    return items[IntPrompt.ask(label, choices=[str(i) for i in range(1, len(items)+1)]) - 1]


def show_aps(aps, lab):
    table = Table(title="Detected access points")
    for col in ("#", "BSSID", "CH", "Signal", "ESSID", "Lab"):
        table.add_column(col)
    for i, ap in enumerate(aps, 1):
        table.add_row(
            str(i), ap.bssid, ap.channel, ap.signal, ap.essid or "<hidden>",
            "[green]ALLOWED[/green]" if lab.is_allowed_ap(ap) else "[dim]ignored[/dim]"
        )
    console.print(table)


def show_stations(stations):
    table = Table(title="Stations for selected AP")
    for col in ("#", "MAC", "BSSID", "Signal"):
        table.add_column(col)
    for i, station in enumerate(stations, 1):
        table.add_row(str(i), station.mac, station.bssid, station.signal)
    console.print(table)


def main():
    banner()
    lab = LabConfig()

    interfaces = list_wifi_interfaces()
    if not interfaces:
        console.print("[bold red]No Wi-Fi interfaces were found.[/bold red]")
        return

    interface = choose(interfaces, "Wi-Fi interfaces", "Select an interface")
    monitor_interface = None

    try:
        if not Confirm.ask(f"Switch [bold]{interface}[/bold] to monitor mode?"):
            return

        monitor_interface = enable_monitor_mode(interface)
        console.print(f"[green]Monitor mode enabled:[/green] {monitor_interface}")

        console.print("[yellow]Scanning passively for 15 seconds...[/yellow]")
        csv_file = scan(monitor_interface, seconds=15)

        aps, stations = parse_airodump_csv(csv_file)
        if not aps:
            console.print("[yellow]No access points were detected.[/yellow]")
            return

        show_aps(aps, lab)

        selected_ap = choose(
            aps,
            "Detected access points",
            "Select your AP",
)
        
        target_stations = [
            s for s in stations
            if s.bssid.upper() == selected_ap.bssid.upper()
        ]

        if not target_stations:
            console.print("[yellow]No stations were detected for this AP.[/yellow]")
            return

        show_stations(target_stations)
        selected_station = choose(
            target_stations,
            "Detected stations",
            "Select a station",
        )

        if not lab.is_allowed_station(selected_station, selected_ap):
            console.print("[bold red]Target validation failed.[/bold red]")
            return

        console.print(Panel(
            f"[bold green]TARGET VALIDATED[/bold green]\n\n"
            f"AP: {selected_ap.bssid}\n"
            f"Channel: {selected_ap.channel}\n"
            f"Station: {selected_station.mac}",
            border_style="green",
        ))

        console.print(
            "\n[cyan]Active testing is intentionally not automated in this build.[/cyan]\n"
            "[dim]Use the validated target information only within your authorized lab.[/dim]"
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
    except Exception as exc:
        console.print(f"\n[bold red]Error:[/bold red] {exc}")
    finally:
        if monitor_interface:
            try:
                restore_managed_mode(monitor_interface)
                console.print("[green]Interface restored to managed mode.[/green]")
            except Exception as exc:
                console.print(f"[yellow]Could not restore interface automatically: {exc}[/yellow]")


if __name__ == "__main__":
    main()
