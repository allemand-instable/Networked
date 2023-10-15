from parameters import Parameters
import InquirerPy.validator as ipv
import InquirerPy.containers as ipc
import InquirerPy.prompts as ipp
from InquirerPy import inquirer
import InquirerPy.base.control as ipbc
import InquirerPy.base.complex as ipbcomplex
import InquirerPy.base.list as ipbl
import InquirerPy.base.simple as ipbs
from InquirerPy.separator import Separator
import InquirerPy.utils as ipu

from view_base import BaseView


class View_SelectDNS(BaseView):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)
