from common.CLI.module.root_module import RootModule
from common.CLI.action import ActionFactory, ActionBuilder
from common.CLI.interface import InterfaceHandler, Interface, UserInterface

root_program_module = RootModule(
    name = "root",
    description = f'CLI for secure management of dotEnv in a project.',
    help_str = f'CLI for secure management of dotEnv in a project.',
)

# root_program_module.activate_debug_options()

def register_base_modules() -> None:
    global root_program_module
    from . import modules as module
    root_program_module += module.create
    root_program_module += module.list_elements
    
    # from .modules.test import TestCommand
    # root_program_module += TestCommand

def register_base_interfaces() -> None:
    global root_program_module
    from . import interfaces as interface
    root_program_module.add_interface(interface.CLIInterface)
    root_program_module.add_interface(interface.ColoramaInterface)

def register_modules() -> None:
    register_base_modules()
    register_base_interfaces()
    
def finalize_app() -> RootModule:
    global root_program_module
    register_modules()
    return root_program_module

app = finalize_app()