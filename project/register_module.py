from base import moduleRegistry as reg
from common.CLI.module import ModuleType, CLImodule

def run_cli() -> None:
    reg()

def register_modules() -> None:
    # Root module
    from base.root_module import RootModule
    from base.config import ROOT_MODULE_NAME
    reg.register_module(RootModule(), ModuleType.root, ROOT_MODULE_NAME)
    
    # user interfaces
    