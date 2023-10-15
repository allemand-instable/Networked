from view_base import BaseView
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


from view_select_action import View_SelectAction


class View_SplashScreen(BaseView):
    def __init__(self, parameters: Parameters) -> None:
        super().__init__(parameters)

    def prompt_user(self) -> bool:

        inquery = inquirer.confirm("PRESS y TO CONTINUE")
        res = inquery.execute()
        print(res)
        return res

    def match_prompt_result(self, prompt_result: bool):
        print(prompt_result)
        if prompt_result:
            print("good")
            return View_SelectAction(self.parameters)
        else:
            print("bad")
            quit()

    def run(self):
        self.match_prompt_result(self.prompt_user())
        return
