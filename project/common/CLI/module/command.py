from .module_abstract import ModuleAbstract
from .module import Module

# from common.CLI.option import OptionAbstract
# from common.CLI.interface import UserInterface, UIDataDriven, UIMenuDriven


class Command(ModuleAbstract):
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def execute(self, *args, **kwargs):
        pass