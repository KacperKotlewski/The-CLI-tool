from common.CLI.module.root_module import RootModule
from common.CLI.action import ActionFactory, ActionBuilder

root_program_module:RootModule = RootModule(
    name = "root",
    description = f'CLI for secure management of dotEnv in a project.',
    help_str = f'CLI for secure management of dotEnv in a project.',
)

def register_base_modules() -> None:
    global root_program_module
    from . import modules as module
    root_program_module += module.create
    root_program_module += module.list_elements

def register_base_interfaces() -> None:
    # Root.interface_handler += Interface()
    pass

def register_modules() -> None:
    register_base_modules()
    register_base_interfaces()
    
def finalize_app() -> RootModule:
    global root_program_module
    register_modules()
    return root_program_module

app = finalize_app()