from base import moduleRegistry as reg

def run_cli() -> None:
    reg()

def register_modules() -> None:
    # Root module
    from base.root_module import RootModule
    reg.register_module(RootModule())
    
    # user interfaces
    