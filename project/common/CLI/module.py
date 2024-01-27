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
        info = ""
        if len(self.options) > 0:
            info += f"\nOptions:\n"
            strlen = max([opt.get_details_len() for opt in self.options])
            
            info += "\n".join([f'  {opt.get_stylized_details(strlen)}' for opt in self.options]) +"\n"
            
        if len(self.commands) > 0:
            info += f"\nCommands:\n"
            strlen = max([len(comm.command) for comm in self.commands])
            
            info += "\n".join([f'  {comm.command:<{strlen}s}\t\t{comm.short_desc}' for comm in self.commands])
            
        return info