import os
from typing import List

def execute_commands(commands : List[str] | str) -> None:
    if isinstance(commands, str):
        os.system(commands)
    elif isinstance(commands, list) :
        for command in commands:
            os.system(command)
    else :
        raise TypeError("wrong type for commands argument")
    return