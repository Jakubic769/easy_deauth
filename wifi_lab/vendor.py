import re
from urllib.request import Request,urlopen
MAC_RE=re.compile(r'^[0-9A-F]{2}(:[0-9A-F]{2}){5}$')
def normalize_mac(mac): return mac.strip().upper().replace('-',':')
def lookup_vendor(mac):
    v=normalize_mac(mac)
    if not MAC_RE.match(v): return 'Unknown'
    try:
        req=Request(f'https://api.macvendors.com/{v[:8]}',headers={'User-Agent':'EasyWiFiLab/1.0'})
        with urlopen(req,timeout=3) as r: return r.read().decode('utf-8',errors='replace').strip() or 'Unknown'
    except Exception: return 'Unknown'
