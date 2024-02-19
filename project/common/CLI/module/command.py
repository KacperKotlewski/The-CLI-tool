from abc import ABC, abstractmethod
import typing
from .module_abstract import ModuleAbstract
from common.CLI.option import OptionHandler
from common.CLI.action import ActionHandler

# from common.CLI.option import OptionAbstract
# from common.CLI.interface import UserInterface, UIDataDriven, UIMenuDriven

class Command(ModuleAbstract):
    action: typing.Callable = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _extra_options_and_actions(self) -> None:
        super()._extra_options_and_actions()
        
    def bad_command_action(self, *args) -> None:
        return super().bad_command_action(*args)
    
    def print_help_usage_action(self, *args) -> None:
        return super().print_help_usage_action(*args)
    
    def _validate(self) -> None:
        self._validate_action()
        return super()._validate()
    
    def _validate_action(self) -> None:
        if self.action is None:
            raise ValueError("Command action is not assigned.")
    
    def execute(self, *args) -> None:
        super().execute(*args)


