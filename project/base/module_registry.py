import typing
from typing import Any
from common.CLI.handler import CLI_Module_Handler, CLI_Model

from .base_cli_module import baseCLI

class CLIHandlerRegistry(CLI_Module_Handler):
    def __init__(self, modules: typing.List[CLI_Model] = list()):
        super().__init__(modules)
        self.register_module(baseCLI())
    
    def register_module(self, module: CLI_Model) -> None:
        if module.module_name in self.modules:
            raise ValueError(f"Module with name {module.module_name} already registered")
        
        self.modules[module.module_name] = module
        self._validate_modules()
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        base_module = self.get_module("base")
        base_module()