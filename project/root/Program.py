from common.CLI.module.root_module import RootModule
from common.CLI.action import ActionFactory, ActionBuilder
import sys
import os

    # name = "root",
    # description: str = None
    # help_str: str = None
    # option_handler: OptionHandler = None
    # current_user_interface: 'UserInterface' = None
    # action_handler: ActionHandler = None

Root = RootModule(
    name = "root",
    description = f'Use "{sys.argv[0]} -h" or "{sys.argv[0]} --help" to display the help message.',
    details = "CLI for secure management of dotEnv in a project.",
    help_str = f'Usage: {sys.argv[0]} COMMAND [OPTIONS] [ARGUMENTS]',
)

# # action to print and root description if no arguments are passed
dry_run_action = ActionBuilder()
dry_run_action.set_name("dry_run")
dry_run_action.set_function(lambda: print(Root.description))
dry_run_action.set_condition(lambda: len(sys.argv) == 1)

Root.action_handler += dry_run_action.build()
    

def register_base_modules() -> None:
    # Root.module_handler += Module()
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