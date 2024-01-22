import typing
from common.CLI.model import CLI_Model

class CLI_Module_Handler:
    modules: typing.Dict[str, CLI_Model] = {}
    
    def __init__(self, modules: typing.List[CLI_Model]):
        self.modules = {module.module_name: module for module in modules}
        self.__validate_modules()
        
    def __validate_modules(self) -> None:
        if not isinstance(self.modules, dict):
            raise ValueError(f"modules {self.modules} is not a dict")
        
        if not all(isinstance(module, CLI_Model) for module in self.modules.values()):
            raise ValueError(f"modules {self.modules} is not a dict of CLI_Model")
        
        self.__validate_keys()
        
    def __validate_keys(self) -> None:
        keys = [key for module in self.modules.values() for arg in module.arguments for key in arg.key]
        if len(keys) != len(set(keys)):
            duplicate = set([key for key in keys if keys.count(key) > 1])
            raise ValueError(f"Duplicate keys found in keys, value of key is: {duplicate}")
        
    def get_module(self, module_name: str) -> CLI_Model:
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
    
    def get_help_info_for_argument(self, module_name: str, argument_name: str) -> str:
        return self.get_module(module_name).get_argument_help_info(argument_name)
    
    def run_model(self, module_name: str, arguments: typing.List[str]) -> None:
        module = self.get_module(module_name)
        module.run(arguments)