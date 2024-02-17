from .module_abstract import ModuleAbstract
from .module_handler import ModuleHandler
from .command import Command

import typing

class Module(ModuleAbstract):
    module_handler: ModuleHandler = None
    
    def __init__(self, **data) -> None:
        self.module_handler = ModuleHandler()
        super().__init__(**data)
        
    def _validate(self) -> None:
        """
        _validate validates the module.
        """
        self._validate_hanlder()
        return super()._validate()
    
    def _validate_hanlder(self) -> None:
        """
        _validate_hanlder validates the module handler.
        
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
        name = args[0]
        args = args[1:]
        return self.module_handler.execute(name, *args)