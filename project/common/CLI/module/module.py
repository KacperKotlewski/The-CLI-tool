from .module_abstract import ModuleAbstract
from .module_handler import ModuleHandler, ModuleNotFound
from .command import Command

from pydantic import Field

import typing

class Module(ModuleAbstract):
    module_handler: ModuleHandler = None
    
    def bad_command_action(self, *args) -> None:
        return super().bad_command_action(*args)
    
    def print_help_usage_action(self, *args) -> None:
        return super().print_help_usage_action(*args)
    
    def __init__(self, **data) -> None:
        data['module_handler'] = ModuleHandler()
        super().__init__(**data)
        
    def get_usage_args(self) -> str:
        text = ""
        
        if len(self.module_handler) > 0:
            text += f" [COMMAND]"
             
        return text + super().get_usage_args()
        
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
            fetch_module = self.module_handler.get(name)
            return fetch_module.execute(*args[1:])
        except ModuleNotFound as e:
            super().execute(*args)
    
    
    
    def get_child_info(self) -> str:
        info = super().get_child_info()
        
        if len(self.module_handler) > 0:
            info += f"\nCommands:\n"
            
            strlen = max([len(opt.__repr__()[0]) for opt in self.module_handler])
            
            info += "\n".join(self.module_handler.stylized_representation(first_str_length = strlen)) +"\n"
            
        return info
    
    def inherit_from(self, module: ModuleAbstract) -> None:
        super().inherit_from(module)
        
        for mod in self.module_handler.items:
            mod.inherit_from(self)
    
    def add_module(self, module: ModuleAbstract) -> None:
        """
        add adds a module to the module handler.
        
        Args:
            module (ModuleAbstract): The module to add to the module handler.
        """
        module.inherit_from(self)
        self.module_handler.add(module)
    
    def __add__(self, other: typing.Union[ModuleAbstract, typing.List[ModuleAbstract], ModuleHandler]) -> 'Module':
        """
        __add__ adds a module to the module handler.
        
        Args:
            other (Union[ModuleAbstract, List[ModuleAbstract]]): The module to add to the module handler.
            
        Returns:
            Module: The module with the added module.
        """
        if isinstance(other, ModuleAbstract):
            other.inherit_from(self)
            self.add_module(other)
            
        elif isinstance(other, list):
            for module in other:
                self.__add__(module)
            
        elif isinstance(other, ModuleHandler):
            self.__add__(other.items)
            
        return self