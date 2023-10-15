from typing import Dict, LiteralString, Literal, List, Tuple, Optional, Self, Any, Type, Protocol, Callable
from enum import StrEnum, Enum
from platform import system
from wmi import _wmi_object

IP_List = List[str]
DNS_Dict_Key = Literal["ipv4"] | Literal["ipv6"] | Literal["name"]
DNS_Dict = Dict[DNS_Dict_Key, IP_List]
ALL_DNS_DICTS = Dict[str, DNS_Dict]


class OperatingSystem(StrEnum):
    apple = "Darwin"
    windows = "Windows"
    linux = "Linux"


NetworkService_ID = str
NetworkService_apple = str
NetworkService_windows = _wmi_object
NetworkService = NetworkService_windows | NetworkService_apple

NetworkServices_windows = Dict[str, NetworkService_windows]
NetworkServices_apple = List[NetworkService_apple]
NetworkServices = NetworkServices_windows | NetworkServices_apple


class NetConnectionStatus(Enum):
    # Adapter is disconnected
    Disconnected = 0
    # Adapter is connecting
    Connecting = 1
    # Adapter is connected
    Connected = 2
    # Adapter is disconnecting
    Disconnecting = 3
    # Adapter hardware is not present
    HardwareNotPresent = 4
    # Adapter hardware is disabled
    HardwareDisabled = 5
    # Adapter has a hardware malfunction
    HardwareMalfunction = 6
    # Media is disconnected
    MediaDisconnected = 7
    # Adapter is authenticating
    Authenticating = 8
    # Authentication has succeeded
    AuthenticationSucceeded = 9
    # Authentication has failed
    AuthenticationFailed = 10
    # Address is invalid
    InvalidAddress = 11
    # Credentials are required
    CredentialsRequired = 12
    # Other unspecified state
    Other = 13

    @staticmethod
    def reverse_map(number: int) -> str:
        match number:
            case 0:
                return "Disconnected"
            case 1:
                return "Connecting"
            case 2:
                return "Connected"
            case 3:
                return "Disconnecting"
            case 4:
                return "HardwareNotPresent"
            case 5:
                return "HardwareDisabled"
            case 6:
                return "HardwareMalfunction"
            case 7:
                return "MediaDisconnected"
            case 8:
                return "Authenticating"
            case 9:
                return "AuthenticationSucceeded"
            case 10:
                return "AuthenticationFailed"
            case 11:
                return "InvalidAddress"
            case 12:
                return "CredentialsRequired"
            case 13:
                return "Other"
            case _:
                return "Unknown"


isEnabled = (NetConnectionStatus.Connected.value,
             NetConnectionStatus.MediaDisconnected.value)
isDisabled = (NetConnectionStatus.Disconnected.value,
              NetConnectionStatus.HardwareDisabled.value)
