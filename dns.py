import tomlkit
from parameters import Parameters
from custom_types import OperatingSystem, DNS_Dict, ALL_DNS_DICTS, DNS_Dict_Key, IP_List
from command_execution import execute_commands


class DNS():

    def __init__(self, params: Parameters):
        self.params = params

    def change_dns(self, network_card: str, dns: DNS_Dict) -> None:
        """given a network card and a dns dictionary, change the dns of the network card by executing the right command according to the operating system

        ➤ if name is default : sets dns to default on the network card or network service

        Args:
            network_card (str): name of network card or service
            dns (DNS_Dict): Dict containing the name, ipv4, ipv6 addresses of a DNS

        Raises:
            NotImplemented: linux not implemented
            ValueError: other OS
        """
        match dns["name"]:
            # default dns == no custom dns
            case "Default":
                match self.params.operating_system:
                    case OperatingSystem.apple:
                        command = f"networksetup -setdnsservers {network_card} empty"

                        flush_command = "dscacheutil -flushcache; killall -HUP mDNSResponder"
                        commands = [command, flush_command]
                    case OperatingSystem.windows:
                        command_ipv4 = f"netsh interface ipv4 set dnsservers name='{network_card}' source=dhcp"
                        command_ipv6 = f"netsh interface ipv6 set dnsservers name='{network_card}' source=dhcp"
                        flush_command = "ipconfig/flushdns"
                        commands = [command_ipv4, command_ipv6, flush_command]
                    case OperatingSystem.linux:
                        raise NotImplemented("Linux not implemented yet")
                    case _:
                        raise ValueError("Unknown operating system")
            # not the default dns server
            case _:
                match self.params.operating_system:

                    case OperatingSystem.apple:
                        command = f"networksetup -setdnsservers {network_card} {dns['ipv4'][0]} {dns['ipv4'][1]} {dns['ipv6'][0]} {dns['ipv6'][1]}"
                        flush_command = "ipconfig/flushdns"
                        get_dns_command = f"networksetup -getdnsservers {network_card}"

                        commands = [command, flush_command, get_dns_command]

                    case OperatingSystem.windows:
                        commands = []
                        for ip_type in dns:
                            if ip_type != "name":
                                command_primary = f"netsh interface {ip_type} set dns '{network_card}' static {dns['ipv4'][0]}"
                                command_secondary = f"netsh interface {ip_type} add dns '{network_card}' {dns['ipv4'][1]} Index=2"
                                commands.append(command_primary)
                                commands.append(command_secondary)
                        flush_command = "ipconfig/flushdns"

                        commands.append(flush_command)

                    case OperatingSystem.linux:
                        raise NotImplemented("Linux not implemented yet")

                    case _:
                        raise ValueError("Unknown operating system")
        execute_commands(commands)

    def save_custom_dns_to_toml(self, dns_key: str, dns: DNS_Dict):
        """adds the following entry to the config file :

        [DNS.dns_key]
        name = dns["name"]
        ipv4 = dns["ipv4"]
        ipv6 = dns["ipv6"]

        Args:
            dns_key (str): entry key for the dns dict
            dns (DNS_Dict): a dict containing 
                ➤ name
                ➤ ipv4 (pair)
                ➤ ipv6 (pair)
        """
        # ⚠️ tomllib reads as bytes, but tomlkit reads and writes as text
        # rb --> rt
        # wb --> wt
        with open(self.params.settings_path, mode="rt", encoding="utf-8") as file:
            settings = tomlkit.load(file)

        tab = tomlkit.table()
        tab.add("name", dns["name"])
        tab.add("ipv4", dns["ipv4"])
        tab.add("ipv6", dns["ipv6"])

        #        [ DNS . dns_key ]
        settings["DNS"].add(dns_key, tab)

        with open(self.params.settings_path, mode="wt", encoding="utf-8") as file:
            tomlkit.dump(settings, file)
