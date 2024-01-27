import typing
from typing import Any
from common.CLI.handler import CLI_Module_Handler, CLImodule
from common.CLI.module import ModuleType
from .config import ROOT_MODULE_NAME

class CLIHandlerRegistry(CLI_Module_Handler):
    def __init__(self, modules: typing.List[CLImodule] = list()):
        super().__init__(modules)
    
    def register_module(self, module: CLImodule, overridden_module_type: ModuleType=None, overridden_module_name:str=None) -> None:
        if overridden_module_name != None:
            module.module_name = overridden_module_name
        if overridden_module_type != None:
            module.module_type = overridden_module_type
        
        if module.module_name in self.modules:
            raise ValueError(f"Module with name {module.module_name} already registered")
        
        if module.module_type == ModuleType.root and len(self.filter_by_type(ModuleType.root).modules) > 0:
            raise ValueError(f"Root module already registered")
        
        self.modules[module.module_name] = module
        self._validate_modules()
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        roots_handler = self.filter_by_type(ModuleType.root)
        if len(roots_handler.modules) > 0:
            root_module = roots_handler.get_module(ROOT_MODULE_NAME)
        
            root_module()