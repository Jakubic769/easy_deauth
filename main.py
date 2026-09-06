#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt
from wifi_lab.interfaces import list_wireless_interfaces, set_monitor_mode, set_managed_mode
from wifi_lab.scanner import scan
from wifi_lab.parser import parse_scan
from wifi_lab.vendor import lookup_vendor, normalize_mac

console=Console()

def choose_interface():
    xs=list_wireless_interfaces()
    if not xs: raise SystemExit('No wireless interfaces found.')
    t=Table(title='Wireless interfaces'); t.add_column('#'); t.add_column('Interface'); t.add_column('Mode')
    for i,x in enumerate(xs,1): t.add_row(str(i),x.name,x.mode)
    console.print(t); return xs[IntPrompt.ask('Choose adapter',choices=[str(i) for i in range(1,len(xs)+1)])-1].name

def choose_ap(aps):
    if not aps: raise SystemExit('No access points detected.')
    t=Table(title='Detected access points')
    for c in ['#','BSSID','Channel','Signal','ESSID']: t.add_column(c)
    for i,a in enumerate(aps,1): t.add_row(str(i),a.bssid,str(a.channel),str(a.signal),a.essid or '<hidden>')
    console.print(t); return aps[IntPrompt.ask('Choose AP',choices=[str(i) for i in range(1,len(aps)+1)])-1]

def choose_station(stations,ap):
    if not stations: console.print('[yellow]No stations associated with this BSSID were detected.[/yellow]'); return None
    t=Table(title=f'Stations associated with {ap.bssid}')
    for c in ['#','Station MAC','Vendor','BSSID','Signal']: t.add_column(c)
    for i,s in enumerate(stations,1): t.add_row(str(i),s.mac,lookup_vendor(s.mac),s.bssid,str(s.signal))
    console.print(t); return stations[IntPrompt.ask('Choose station',choices=[str(i) for i in range(1,len(stations)+1)])-1]

def main():
    console.print('[bold cyan]Easy WiFi Lab[/bold cyan]')
    iface=choose_interface(); mon=None
    try:
        mon=set_monitor_mode(iface); console.print(f'[green]Monitor interface: {mon}[/green]')
        console.print('[cyan]Passive scan: 15 seconds...[/cyan]')
        raw=scan(mon,15); aps,stations=parse_scan(raw)
        ap=choose_ap(aps); bssid=normalize_mac(ap.bssid)
        linked=[s for s in stations if normalize_mac(s.bssid)==bssid]
        st=choose_station(linked,ap)
        if st is None: return
        if normalize_mac(st.bssid)!=bssid:
            console.print('[red]Target validation failed: station is not associated with selected BSSID.[/red]'); return
        console.print('[bold green]TARGET SELECTED[/bold green]')
        console.print(f'AP: {ap.essid or "<hidden>"} | BSSID: {ap.bssid} | Station: {st.mac} | Vendor: {lookup_vendor(st.mac)}')
        console.print('[dim]Active packet-disruption actions are not automated.[/dim]')
    finally:
        if mon:
            try: set_managed_mode(mon)
            except Exception as e: console.print(f'[yellow]Could not restore managed mode: {e}[/yellow]')

if __name__=='__main__': main()
