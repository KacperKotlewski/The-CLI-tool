from abc import ABC, abstractmethod
import typing
from .module_abstract import ModuleAbstract

class Command(ModuleAbstract):
    base_action: typing.Callable = None
    root_module: typing.Optional['Command'] = None
    
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
        if self.base_action is None:
            raise ValueError("Command action is not assigned.")
    
    def run_base_action(self, *args, **kwargs) -> typing.Any:
        try:
            from .root_module import RootModule
            if self.root_module is not None and isinstance(self.root_module, RootModule):
                self._ui = self.root_module.get_ui()
        except ImportError:
            pass
        return super().run_base_action(*args, **kwargs)
    
    def execute(self, *args):
        return super().execute(*args)

    def command(self, *args, **kwargs) -> typing.Any:
        return super().command(*args, **kwargs)

