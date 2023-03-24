from custom_types import OperatingSystem
from parameters import Parameters
from command_execution import execute_commands
from platform import system
if system() == OperatingSystem.windows :
    import wmi
from typing import List, Dict, Tuple
import subprocess

class NetworkCard():
    def __init__(self, parameters : Parameters) -> None:
        
        
        self.parameters = parameters
        #self.update_network_cards()
        #self.update_available_network_cards()
        
        return
    
    @staticmethod
    def __apple_get_network_cards() -> List[str]:
        """Returns a list of all hardware network cards names on the computer

        Returns:
            List[str]: Network Cards
        """
        return subprocess.check_output(r'networksetup -listallhardwareports | grep "Hardware Port:" | sed "s/Hardware Port: //"', shell=True).decode("utf-8").split("\n")[:-1]
    
    @staticmethod
    def __apple_get_network_services() -> List[str]:
        return subprocess.check_output(r'networksetup -listallnetworkservices', shell=True).decode("utf-8").split("\n")[1:-1]
    
    @staticmethod
    def __apple_get_available_services() -> List[str]:
        """Returns a list of the names of available Services
        Note : An asterisk (*) denotes that a network service is disabled.

        Returns:
            List[str]: Available Network Services
        """
        return [service for service in NetworkCard.__apple_get_network_services() if service[0] != "*"]
    
    @staticmethod
    def __apple_get_enabled_and_disabled_services() -> Tuple[List[str], List[str]]:
        """Returns 2 Lists of network service names : 1st List : Enabled Services, 2nd List : Disabled Services

        Returns:
            Tuple[List[str], List[str]]: (Enabled Services, Disabled Services)
        """
        services = NetworkCard.__apple_get_network_services()
        return [service for service in services if service[0] != "*"],   [service[1:] for service in services if service[0] == "*"]
    
    @staticmethod
    def __apple_enable_network_service(network_service_name : str):
        command = f"networksetup -setnetworkserviceenabled '{network_service_name}' on"
        execute_commands(command)
        return
    
    @staticmethod
    def __apple_disable_network_service(network_service_name : str):
        command = f"networksetup -setnetworkserviceenabled '{network_service_name}' off"
        execute_commands(command)
        return
    
    @staticmethod
    def __windows_get_network_cards() -> Dict :
        """
        Returns:
            Dict: all network cards on the machine
        """
        network_cards = {adapter.NetConnectionID : adapter for adapter in wmi.WMI().query("select * from Win32_NetworkAdapter")}
        return network_cards
    
    def __windows_update_network_cards(self) -> None :
        self.network_cards = self.__windows_get_network_cards()
        return 
    
    @staticmethod
    def __windows_get_available_network_cards() -> Dict:
        """
        Returns:
            Dict: all AVAILABLE network cards on the machine
        """
        available_network_cards = {adapter.NetConnectionID : adapter for adapter in wmi.WMI().query("select * from Win32_NetworkAdapter") if adapter.NetConnectionID }
        return available_network_cards

    def __windows_update_available_network_cards(self) -> None:
        self.available_network_cards = self.__windows_get_available_network_cards()
        return
    
    def __windows_changer_carte(self, ancienne_carte_id, nouvelle_carte_id):
        self.__windows_desactiver_carte(ancienne_carte_id)
        self.__windows_activer_carte(nouvelle_carte_id)
        return
    
    def __windows_desactiver_carte(self, carte_id):
        if carte_id in self.network_cards :
            if self.network_cards[carte_id].NetEnabled :
                self.network_cards[carte_id].Disable()
            else :
                print(f'{carte_id} est déjà désactivée')
        else :
            raise IndexError(f"{carte_id} n'existe pas dans self.network_cards") 
        return
    
    def __windows_activer_carte(self, carte_id):
        if carte_id in self.network_cards :
            if self.network_cards[carte_id].NetEnabled:
                print(f'{carte_id} est déjà activée !')
            else:
                self.network_cards[carte_id].Enable()
        else :
            raise IndexError(f"{carte_id} n'existe pas dans self.network_cards")
        return
    
    def __windows_relancer_carte(self, carte_id):
        self.__windows_desactiver_carte(carte_id)
        self.__windows_activer_carte(carte_id)
        return
    
    def __windows_choisir_carte(self, carte_choisie_id):
        for carte_id, carte in self.network_cards.items() :
            if carte_id != carte_choisie_id :
                self.__windows_desactiver_carte(carte)
            else :
                self.__windows_activer_carte(carte)
        return
    
if __name__ == "__main__":
    network_card = NetworkCard(Parameters())
    print(network_card._NetworkCard__apple_get_network_cards())
    print(network_card._NetworkCard__apple_get_available_services())
    print(network_card._NetworkCard__apple_get_enabled_and_disabled_services())
    print(network_card._NetworkCard__apple_enable_network_service("Thunderbolt Bridge"))