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

from abc import abstractclassmethod, abstractmethod, abstractstaticmethod
from abc import ABCMeta as AbstractClass
from typing import Any


class BaseView(metaclass=AbstractClass):
    
    style_dict = {
        "questionmark": "#e5c07b bold",
        "answermark": "#e5c07b bold",
        "answer": "#61afef italic",
        "input": "#98c379",
        "question": "",
        "answered_question": "",
        "instruction": "#abb2bf",
        "long_instruction": "#abb2bf",
        "pointer": "#61afef",
        "checkbox": "#98c379",
        "separator": "",
        "skipped": "#5c6370",
        "validator": "bg:#ff7979 fg:#1e272e bold",
        "marker": "#e5c07b",
        "fuzzy_prompt": "#c678dd",
        "fuzzy_info": "#abb2bf",
        "fuzzy_border": "#4b5263",
        "fuzzy_match": "#c678dd",
        "spinner_pattern": "#e5c07b",
        "spinner_text": "",
    }
    
    style = ipu.get_style(style=style_dict)
    
    def __init__(self, parameters : Parameters) -> None:
        
        self.parameters = parameters
    
    @abstractmethod
    def prompt_user(self):
        pass
    @abstractmethod
    def match_prompt_result(self, prompt_result):
        pass
    