from .module_abstract import ModuleAbstract
from common.models.base import BaseModel

import typing

class ModuleNotFound(Exception):
    pass

class ModuleHandler(BaseModel):
    modules: typing.List[ModuleAbstract] = list()
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    def _validate(self) -> None:
        self._validate_modules()
        
    def _validate_modules(self) -> None:
        list_of_names = [module.name for module in self.modules]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"ModuleHandler has duplicate module names: \n{list_of_names}")
        
        for module in self.modules:
            module._validate()
            
    def add_module(self, module: ModuleAbstract) -> None:
        if module not in self.modules:
            self.modules.append(module)
            self._validate_modules()
            
    def remove_module(self, module: ModuleAbstract) -> None:
        if module in self.modules:
            self.modules.remove(module)
            self._validate_modules()
            
    def get_module(self, name: str) -> ModuleAbstract:
        for module in self.modules:
            if module.name == name:
                return module
        raise ModuleNotFound(f"Module {name} not found.")
    
    def __iadd__(self, module: typing.Union[ModuleAbstract, typing.List[ModuleAbstract]]) -> 'ModuleHandler':
        if isinstance(module, list):
            for mod in module:
                self.add_module(mod)
        else:
            self.add_module(module)
        return self
    
    def execute(self, name: str, *args) -> typing.Any:
        module = self.get_module(name)
        return module(*args)
    
    def __len__(self) -> int:
        return len(self.modules)