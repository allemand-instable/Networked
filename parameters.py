import tomllib
import platform
from enum import StrEnum
from custom_types import ALL_DNS_DICTS


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    
class Parameters(metaclass = Singleton):
    def __init__(self):
        self.settings_path = "./settings.toml"
        with open(self.settings_path, "rb") as file:
            data = tomllib.load(file)
        self.DNS : ALL_DNS_DICTS = data['DNS']
        
        self.operating_system = platform.system()
        