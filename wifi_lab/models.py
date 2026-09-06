from dataclasses import dataclass
@dataclass
class AccessPoint: bssid:str; channel:str; signal:str; essid:str
@dataclass
class Station: mac:str; bssid:str; signal:str
