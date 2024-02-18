from .module_abstract import ModuleAbstract
from .module_handler import ModuleHandler, ModuleNotFound
from .command import Command

from pydantic import Field

import typing

class Module(ModuleAbstract):
    module_handler: ModuleHandler = None
    
    def __init__(self, **data) -> None:
        data['module_handler'] = ModuleHandler()
        super().__init__(**data)
        
    def _validate(self) -> None:
        """
        _validate validates the module.
        """
        self._validate_handler()
        return super()._validate()
    
    def _validate_handler(self) -> None:
        """
        _validate_handler validates the module handler.
        
        Raises:
            ValueError: If the module handler is not set.
        """
        if self.module_handler is None:
            raise ValueError("Module handler not set.")
        self.module_handler._validate()
        
    def _extra_options_and_actions(self) -> None:
        return super()._extra_options_and_actions()
        
    def execute(self, *args) -> typing.Any:
        """
        execute executes the module.
        
        Args:
            *args: The arguments to be passed to the module.
        """
        try:
            name = args[0] if len(args) > 0 else None
            fetch_module = self.module_handler.get_module(name)
            return fetch_module.execute(*args[1:])
        except ModuleNotFound as e:
            super().execute(*args)
        
        
        
    def get_details(self) -> str:
        info = super().get_details()
        
        try:
            from blessed import Terminal
            term = Terminal()
            width = term.width
        except ImportError:
            import shutil
            width = shutil.get_terminal_size().columns
            
        spaces = {"before": 2, "after": 10}
        
        calc_taken = lambda strlen: spaces["before"] + strlen + spaces["after"]
        
        create_str = lambda text1, text2: (
            " " * spaces["before"] +
            text1 +
            " " * spaces["after"] +
            text2
        )
        
        if len(self.module_handler) > 0:
            info += f"\nCommands:\n"
            info += "\n".join([f" {command.name} - {command.description}" for command in self.module_handler.modules]) +"\n"
            # strlen = max([len(opt.get_keys_str()) for opt in self.option_handler.options])
            
            # taken = calc_taken(strlen)
            
            # create_opt_str = lambda option: create_str(option.get_stylized_keys(strlen), option.spaced_description(taken, width)[taken+1:])
            
            # info += "\n".join([create_opt_str(opt) for opt in self.option_handler.options]) +"\n"
            
        return info