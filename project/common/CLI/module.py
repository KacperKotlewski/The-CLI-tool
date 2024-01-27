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