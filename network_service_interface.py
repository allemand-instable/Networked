from custom_types import OperatingSystem
from custom_types import NetworkService, NetworkService_windows, NetworkService_apple, NetworkService_ID
from custom_types import NetworkServices, NetworkServices_windows, NetworkServices_apple
from custom_types import NetConnectionStatus, isEnabled, isDisabled

from parameters import Parameters
from command_execution import execute_commands
from platform import system
if system() == OperatingSystem.windows:
    import wmi

from typing import List, Dict, Tuple, Callable, Optional
import subprocess

from time import sleep


class NetworkService_Interface():
    def __init__(self, parameters: Parameters) -> None:
        self.parameters = parameters
        self.network_services = self.get_network_services()
        self.enabled_network_services, self.disabled_network_services = self.get_enabled_and_disabled_services()
        # self.update_available_network_services()
        return

    def match_os(self, windows_function: Optional[Callable], apple_function: Optional[Callable], linux_function: Optional[Callable]) -> Callable:
        """Returns the appropriate function according to the target operating system

        Args:
            windows_function (Optional[Callable]): _description_
            apple_function (Optional[Callable]): _description_
            linux_function (Optional[Callable]): _description_

        Raises:
            NotImplemented: _description_
            NotImplemented: _description_
            NotImplemented: _description_
            Exception: _description_

        Returns:
            Callable: _description_
        """
        match self.parameters.operating_system:
            case OperatingSystem.windows:
                if windows_function is None:
                    raise NotImplemented
                else:
                    return windows_function
            case OperatingSystem.apple:
                if apple_function is None:
                    raise NotImplemented
                else:
                    return apple_function
            case OperatingSystem.linux:
                if linux_function is None:
                    raise NotImplemented
                else:
                    return linux_function
            case _:
                raise Exception("unknown operating system")

    def get_available_services(self) -> NetworkServices:
        get_function = self.match_os(windows_function=self.__windows_get_available_network_services,
                                     apple_function=self.__apple_get_available_services,
                                     linux_function=None)
        return get_function()

    def get_network_services(self) -> NetworkServices:
        get_function = self.match_os(windows_function=self.__windows_get_network_services,
                                     apple_function=self.__apple_get_network_services,
                                     linux_function=None)
        return get_function()

    def get_enabled_and_disabled_services(self) -> Tuple[NetworkServices, NetworkServices]:
        get_both_function = self.match_os(
            windows_function=self.__windows_get_enabled_and_disabled_services,
            apple_function=self.__apple_get_enabled_and_disabled_services,
            linux_function=None
        )
        return get_both_function()

    # @property
    # def network_services(self) -> NetworkServices:
    #     return self.get_network_services()

    # @property
    # def available_network_services(self) -> NetworkServices:
    #     return self.get_available_services()

    def enable_service(self, network_service: NetworkService_ID) -> None:
        enable_function = self.match_os(
            windows_function=self.__windows_enable_service,
            apple_function=self.__apple_enable_network_service,
            linux_function=None
        )
        enable_function(network_service)
        return

    def disable_service(self, network_service: NetworkService_ID) -> None:
        disable_function = self.match_os(
            windows_function=self.__windows_disable_service,
            apple_function=self.__apple_disable_network_service,
            linux_function=None
        )
        disable_function(network_service)
        return

    def change_service(self, old_network_service: NetworkService_ID, new_network_service: NetworkService_ID) -> None:
        self.enable_service(new_network_service)
        self.disable_service(old_network_service)
        return

    def restart_network_service(self, network_service) -> None:
        enable_function = self.match_os(
            windows_function=self.__windows_enable_service,
            apple_function=self.__apple_enable_network_service,
            linux_function=None
        )
        disable_function = self.match_os(
            windows_function=self.__windows_disable_service,
            apple_function=self.__apple_disable_network_service,
            linux_function=None
        )
        disable_function(network_service)
        sleep(1)  # makes sure the service is disabled first
        enable_function(network_service)
        return

    def update_enabled_and_disabled_network_services(self):
        self.enabled_network_services, self.disabled_network_services = self.get_enabled_and_disabled_services()
        return

    def update_network_services(self):
        self.network_services = self.get_network_services()
        return

    @staticmethod
    def __apple_get_hardware_network_services() -> NetworkServices_apple:
        """Returns a list of all hardware network cards names on the computer

        Returns:
            List[str]: Network Cards
        """
        return subprocess.check_output(r'networksetup -listallhardwareports | grep "Hardware Port:" | sed "s/Hardware Port: //"', shell=True).decode("utf-8").split("\n")[:-1]

    @staticmethod
    def __apple_get_network_services() -> NetworkServices_apple:
        return subprocess.check_output(r'networksetup -listallnetworkservices', shell=True).decode("utf-8").split("\n")[1:-1]

    @staticmethod
    def __apple_get_available_services() -> NetworkServices_apple:
        """Returns a list of the names of available Services
        Note : An asterisk (*) denotes that a network service is disabled.

        Returns:
            List[str]: Available Network Services
        """
        return [service for service in NetworkService_Interface.__apple_get_network_services() if service[0] != "*"]

    @staticmethod
    def __apple_get_enabled_and_disabled_services() -> Tuple[NetworkServices_apple, NetworkServices_apple]:
        """Returns 2 Lists of network service names : 1st List : Enabled Services, 2nd List : Disabled Services

        Returns:
            Tuple[List[str], List[str]]: (Enabled Services, Disabled Services)
        """
        services = NetworkService_Interface.__apple_get_network_services()
        return [service for service in services if service[0] != "*"],   [service[1:] for service in services if service[0] == "*"]

    @staticmethod
    def __apple_enable_network_service(network_service_name: str) -> None:
        command = f"networksetup -setnetworkserviceenabled '{network_service_name}' on"
        execute_commands(command)
        return

    @staticmethod
    def __apple_disable_network_service(network_service_name: str) -> None:
        command = f"networksetup -setnetworkserviceenabled '{network_service_name}' off"
        execute_commands(command)
        return

    @staticmethod
    def __windows_get_network_services() -> NetworkServices_windows:
        """
        Returns:
            Dict: all network cards on the machine
        """
        network_services = {
            adapter.NetConnectionID: adapter
            for adapter in wmi.WMI().query("select * from Win32_NetworkAdapter")
        }
        return network_services

    # def __windows_update_network_services(self) -> None:
    #     self.network_services = self.__windows_get_network_services()
    #     return

    @staticmethod
    def __windows_get_available_network_services() -> NetworkServices_windows:
        """
        Returns:
            Dict: all AVAILABLE network cards on the machine
        """
        available_network_services = {
            adapter.NetConnectionID: adapter
            for adapter in wmi.WMI().query("select * from Win32_NetworkAdapter")
            if adapter.NetConnectionID
        }
        return available_network_services

    def __windows_get_enabled_and_disabled_services(self) -> Tuple[Optional[NetworkServices_windows], Optional[NetworkServices_windows]]:
        services = self.__windows_get_network_services()
        enabled_services = {
            service.NetConnectionID: service
            for service in services.values()
            if service.NetConnectionStatus in isEnabled
        }
        disabled_services = {
            service.NetConnectionID: service
            for service in services.values()
            if service.NetConnectionStatus in isDisabled
        }
        return (enabled_services, disabled_services)  # type: ignore

    # def __windows_update_available_network_services(self) -> None:
    #     self.available_network_services = self.__windows_get_available_network_services()
    #     return

    def __windows_changer_service(self, old_network_service_id: str, new_network_service_id: str) -> None:
        self.__windows_disable_service(old_network_service_id
                                       )
        self.__windows_enable_service(new_network_service_id
                                      )
        return

    def __windows_disable_service(self, network_service_id: str) -> None:
        if network_service_id in self.network_services:
            if self.network_services[network_service_id].NetEnabled:
                self.network_services[network_service_id].Disable()
            else:
                print(f'{network_service_id} est déjà désactivée')
        else:
            raise IndexError(
                f"{network_service_id} n'existe pas dans self.network_services")
        return

    def __windows_enable_service(self, network_service_id: str) -> None:
        print(f"enabling {network_service_id}...")
        if network_service_id in self.network_services:
            if self.network_services[network_service_id].NetConnectionStatus in isEnabled:
                print(f'{network_service_id} est déjà activée !')
            elif self.network_services[network_service_id].NetConnectionStatus in isDisabled:
                print(
                    f"{network_service_id} is Disabled ({self.network_services[network_service_id].NetConnectionStatus}) : enabling it...")
                print(self.network_services[network_service_id])
                self.network_services[network_service_id].Enable()
                print(
                    self.network_services[network_service_id].NetConnectionStatus)
            else:
                raise Exception(
                    f"Wrong Network Service's status : {self.network_services[network_service_id].NetConnectionStatus}")
        else:
            raise IndexError(
                f"{network_service_id} n'existe pas dans self.network_services")
        return

    def __windows_restart_network_service(self, network_service_id: str) -> None:
        self.__windows_disable_service(network_service_id)
        self.__windows_enable_service(network_service_id)
        return

    def __windows_choose_network_service(self, chosen_network_service_id: str) -> None:
        for network_service_id, service in self.network_services.items():
            if network_service_id != chosen_network_service_id:
                self.__windows_disable_service(service)
            else:
                self.__windows_enable_service(service)
        return


if __name__ == "__main__":
    network_service = NetworkService_Interface(Parameters())
    if system() == OperatingSystem.apple:
        print(
            network_service._NetworkService_Interface__apple_get_network_services()
        )
        print(
            network_service._NetworkService_Interface__apple_get_available_services()
        )
        print(
            network_service._NetworkService_Interface__apple_get_enabled_and_disabled_services()
        )
        print(
            network_service._NetworkService_Interface__apple_enable_network_service(
                "Thunderbolt Bridge")
        )
    elif system() == OperatingSystem.windows:
        from pprint import pprint
        # pprint(network_service.enabled_network_services)
        # print('\nEnabled and Disabled\n')
        # pprint(
        #     network_service._NetworkService_Interface__windows_get_enabled_and_disabled_services())

        # pprint(network_service.network_services)
        # pprint(
        #     {service.NetConnectionID: service.NetConnectionStatus for service in network_service.network_services.values()})

        # les_services = network_service.enabled_network_services
        # print(
        #     f'wifi : {NetConnectionStatus.reverse_map(les_services["Wi-Fi"].NetConnectionStatus)}'
        # )
        # print(
        #     f'Bluetooth Network Connection : {NetConnectionStatus.reverse_map(les_services["Bluetooth Network Connection"].NetConnectionStatus)}'
        # )
        # print(
        #     f'Ethernet : {NetConnectionStatus.reverse_map(les_services["Ethernet"].NetConnectionStatus)}'
        # )
        from elevate import elevate

        elevate()

        enabled, disabled = network_service.get_enabled_and_disabled_services()
        services_all = network_service._NetworkService_Interface__windows_get_network_services()

        # pprint(services_all)
        # print(services_all['Bluetooth Network Connection'].Disable())

        # print(f"ENABLED :\n{enabled}\nDISABLED :\n{disabled}")

        # network_service.enable_service("Ethernet")
        # print(dir(disabled["Ethernet"]))
        # print(disabled["Ethernet"]._methods)
        # disabled["Ethernet"].Enable()
        services_all["Ethernet"].Enable()
