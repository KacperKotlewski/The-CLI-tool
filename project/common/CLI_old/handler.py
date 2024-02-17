import typing
from common.CLI_old.module import CLImodule, ModuleType


class CLI_Module_Handler:
    modules: typing.Dict[str, CLImodule] = {}
    
    def __init__(self, modules: typing.List[CLImodule]):
        self.modules = {module.module_name: module for module in modules}
        self._validate_modules()
        
    def _validate_modules(self) -> None:
        if not isinstance(self.modules, dict):
            raise ValueError(f"modules {self.modules} is not a dict")
        
        if not all(isinstance(module, CLImodule) for module in self.modules.values()):
            raise ValueError(f"modules {self.modules} is not a dict of CLImodule")
        
        self._validate_keys()
        
    def _validate_keys(self) -> None:
        keys = [key.key for module in self.modules.values() for arg in module.options for key in arg.key]
                    
        if len(keys) != len(set(keys)):
            duplicate = set([key for key in keys if keys.count(key) > 1])
            raise ValueError(f"Duplicate keys found in keys, value of key is: {duplicate}")
        
    def get_module(self, module_name: str) -> CLImodule:
        if module_name not in self.modules:
            raise ValueError(f"Module {module_name} not found")
        
        return self.modules[module_name]
    
    def get_modules_names(self) -> typing.List[str]:
        return list(self.modules.keys())
    
    def get_help_info(self) -> str:
        info = "\n\n".join([module.help_info() for module in self.modules.values()])
        return info
    
    def get_help_info_for_module(self, module_name: str) -> str:
        return self.get_module(module_name).help_info()
    
    def get_help_info_for_option(self, module_name: str, option_name: str) -> str:
        return self.get_module(module_name).get_option_help_info(option_name)
    
    def filter_by_type(self, module_type: ModuleType) -> 'CLI_Module_Handler':
        filtered_modules = [module for module in self.modules.values() if module.module_type == module_type]
        return CLI_Module_Handler(modules=filtered_modules)
    
    def run_model(self, module_name: str, options: typing.List[str]) -> None:
        module = self.get_module(module_name)
        module.run(options)