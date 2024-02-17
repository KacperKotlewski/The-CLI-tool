# from .module import CLImodule, ModuleType
from abc import ABC, abstractmethod
import typing

class Interface(ABC):
    interface_name: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.interface_name = self.__class__.__name__
        
    @abstractmethod
    def handle_command(self, command: str, args: typing.List[str]) -> None:
        pass