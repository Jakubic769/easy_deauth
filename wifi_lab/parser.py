import csv
from .models import AccessPoint,Station
def parse_scan(path):
    rows=list(csv.reader(open(path,encoding='utf-8',errors='replace',newline=''))); ai=si=None
    for i,r in enumerate(rows):
        if r and r[0].strip()=='BSSID': ai=i
        elif r and r[0].strip()=='Station MAC': si=i
    aps=[]; sts=[]
    if ai is not None:
        for r in rows[ai+1:]:
            if len(r)<14 or not r[0].strip(): continue
            aps.append(AccessPoint(r[0].strip(),r[3].strip(),r[8].strip(),r[13].strip()))
    if si is not None:
        for r in rows[si+1:]:
            if len(r)<6 or not r[0].strip(): continue
            sts.append(Station(r[0].strip(),r[5].strip(),r[3].strip()))
    return aps,sts
