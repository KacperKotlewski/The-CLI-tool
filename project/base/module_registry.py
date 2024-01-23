import typing
from typing import Any
from common.CLI.handler import CLI_Module_Handler, CLImodule
from common.CLI.module import ModuleType

class CLIHandlerRegistry(CLI_Module_Handler):
    def __init__(self, modules: typing.List[CLImodule] = list()):
        super().__init__(modules)
    
    def register_module(self, module: CLImodule) -> None:
        if module.module_name in self.modules:
            raise ValueError(f"Module with name {module.module_name} already registered")
        
        if module.module_type == ModuleType.root and len(self.filter_by_type(ModuleType.root).modules) > 0:
            raise ValueError(f"Root module already registered")
        
        self.modules[module.module_name] = module
        self._validate_modules()
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        root = self.filter_by_type(ModuleType.root)
        root_names = root.get_modules_names()
        if len(root_names) > 0:
            root_name = root_names[0]
            base_module = root.get_module(root_name)
        
            base_module()