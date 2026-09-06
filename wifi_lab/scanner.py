import subprocess,tempfile
from pathlib import Path
def scan(interface,duration=15):
    with tempfile.TemporaryDirectory(prefix='easy_wifi_lab_') as d:
        p=str(Path(d)/'scan'); subprocess.run(['sudo','timeout',str(duration),'airodump-ng','--write-interval','1','--output-format','csv','--write',p,interface],check=False)
        src=Path(p+'-01.csv')
        if not src.exists(): raise RuntimeError('airodump-ng did not produce a CSV scan file.')
        dst=Path.cwd()/'.easy_wifi_lab_scan.csv'; dst.write_bytes(src.read_bytes()); return dst
