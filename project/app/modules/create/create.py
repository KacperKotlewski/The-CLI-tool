import os
import sys
from common.CLI.module import Module, Command, command
from common.CLI.option import OptionFactory, OptionBuilder, OptionHandler
from common.CLI.module.root_module import RootModule
from common.CLI.interface import UserInterface

create = Module(
    name = "create",
    description = "Create new elements in the project.",
    help_str = "This command creates a new module in the project.",
)