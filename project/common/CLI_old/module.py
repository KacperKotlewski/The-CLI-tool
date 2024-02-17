import enum
from copy import deepcopy

from ._with_options_class import BaseWithOptions
import typing
from . import options as o
from . import commands as c


class ModuleType(enum.Enum):
    root = enum.auto()
    user_interface = enum.auto()
    other = enum.auto()

class CLImodule(BaseWithOptions):
    commands: typing.List[c.Command] = list()
    module_name: str = None
    module_type: ModuleType = ModuleType.other
    
    def get_details(self) -> str:
        info = super().get_details()
        
        if len(self.commands) > 0:
            info += f"\nCommands:\n"
            strlen = max([comm.get_details_len()  for comm in self.commands])
            
            info += "\n".join([f'  {comm.get_stylized_details(strlen)}' for comm in self.commands]) +"\n"
            
        return info
    
    def get_command(self, command_name: str) -> c.Command:
        for command in self.commands:
            if command.name == command_name:
                return command
        raise ValueError(f"command {command_name} not found")