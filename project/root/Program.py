from common.CLI.module.root_module import RootModule
from common.CLI.action import ActionFactory, ActionBuilder
import sys
import os

root:RootModule = RootModule(
    name = "root",
    description = f'CLI for secure management of dotEnv in a project.',
    help_str = f'CLI for secure management of dotEnv in a project.',
)


def register_base_modules() -> None:
    global root
    from . import modules as module
    root += module.create

def register_base_interfaces() -> None:
    # Root.interface_handler += Interface()
    pass

def register_modules() -> None:
    register_base_modules()
    register_base_interfaces()

def run_cli() -> None:
    register_modules()
    args = sys.argv[1:]
    root.execute(*args)