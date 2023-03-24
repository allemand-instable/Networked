from parameters import Parameters
import InquirerPy.validator as ipv
import InquirerPy.containers as ipc
import InquirerPy.prompts as ipp
from InquirerPy import inquirer, prompt
import InquirerPy.base.control as ipbc
import InquirerPy.base.complex as ipbcomplex
import InquirerPy.base.list as ipbl
import InquirerPy.base.simple as ipbs
from InquirerPy.separator import Separator
import InquirerPy.utils as ipu

from typing import List, Dict, Optional


from view_base import BaseView

class View_SelectAction(BaseView) :
    
    actions : List[ipbc.Choice | Separator] = [
        ipbc.Choice( value="dns-change", name="Change DNS server"),
        
        Separator(),
        
        ipbc.Choice(value="network_card-enable", name="Enable a Network Card"),
        ipbc.Choice(value="network_card-disable", name="Disable a Network Card"),
        ipbc.Choice(value="network_card-solo", name="Change Network Card"),
        
        Separator(),
        
        ipbc.Choice( value="quit", name="Quit" )
    ]
    
    
    def  __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)
    
    def prompt_user(self) -> str:
        inquery = inquirer.select(  message = "Please select action :",
                                    choices=self.actions,
                                    border=True,
                                    validate= ipv.EmptyInputValidator(),
                                    instruction="select an action and press Enter"
                                  )
        
        return inquery.execute()
    
    def match_prompt_result(self, prompt_result : str):
        match prompt_result :
            case "network_card-enable" :
                raise NotImplemented
            case "network_card-disable" :
                raise NotImplemented
            case "network_card-solo" :
                raise NotImplemented
            case "dns-change" :
                raise NotImplemented
            case "quit" :
                raise NotImplemented