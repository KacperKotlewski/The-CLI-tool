from common.CLI.module.root_module import RootModule
from common.CLI.action import ActionFactory, ActionBuilder
import sys
import os

Root = RootModule(
    name = "root",
    description = f'Use "{sys.argv[0]} -h" or "{sys.argv[0]} --help" to display the help message.',
    details = "CLI for secure management of dotEnv in a project.",
    help_str = f'Usage: {sys.argv[0]} COMMAND [OPTIONS] [ARGUMENTS]',
)

    


def register_base_modules() -> None:
    # from . import modules as module
    # Root.module_handler += module.create
    pass

def register_base_interfaces() -> None:
    # Root.interface_handler += Interface()
    pass

def register_modules() -> None:
    register_base_modules()
    register_base_interfaces()

def run_cli() -> None:
    register_modules()
    args = sys.argv[1:]
    Root.execute(*args)