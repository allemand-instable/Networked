from typing import Dict, LiteralString, Literal, List, Tuple, Optional, Self
from enum import StrEnum

IP_List = List[str]
DNS_Dict_Key = Literal["ipv4"] | Literal["ipv6"] | Literal["name"]
DNS_Dict = Dict[DNS_Dict_Key, IP_List]
ALL_DNS_DICTS = Dict[str, DNS_Dict]


class OperatingSystem(StrEnum):
    apple = "Darwin"
    windows = "Windows"
    linux = "Linux"