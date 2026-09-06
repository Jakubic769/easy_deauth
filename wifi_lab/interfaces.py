import subprocess
from dataclasses import dataclass
@dataclass
class WirelessInterface: name:str; mode:str
def list_wireless_interfaces():
    r=subprocess.run(['iw','dev'],capture_output=True,text=True,check=True); out=[]; cur=None
    for line in r.stdout.splitlines():
        s=line.strip()
        if s.startswith('Interface '): cur=s.split(None,1)[1]; out.append(WirelessInterface(cur,'unknown'))
        elif cur and s.startswith('type '): out[-1].mode=s.split(None,1)[1]
    return out
def set_monitor_mode(i):
    subprocess.run(['sudo','ip','link','set',i,'down'],check=True); subprocess.run(['sudo','iw','dev',i,'set','type','monitor'],check=True); subprocess.run(['sudo','ip','link','set',i,'up'],check=True); return i
def set_managed_mode(i):
    subprocess.run(['sudo','ip','link','set',i,'down'],check=True); subprocess.run(['sudo','iw','dev',i,'set','type','managed'],check=True); subprocess.run(['sudo','ip','link','set',i,'up'],check=True)
