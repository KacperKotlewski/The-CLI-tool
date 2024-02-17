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
        if not self.module_handler:
            raise ValueError("Module handler not set.")
        self.module_handler._validate()
        
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
        