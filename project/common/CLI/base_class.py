import enum
from copy import deepcopy

from common.models.base import BaseModel
import typing
from .argument_classes import Argument, ArgumentComplexity, ArgumentKeyTypes, ArgumentValueTypes, KeyModel, ValueModel


class CLI_Handler(BaseModel):
    arguments: typing.List[Argument] = list()
    module_name: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_arguments()
        
    def _validate_arguments(self) -> None:
        if not isinstance(self.arguments, list):
            raise ValueError(f"Arguments {self.arguments} is not a list")
        
        if not all(isinstance(arg, Argument) for arg in self.arguments):
            raise ValueError(f"Arguments {self.arguments} is not a list of Arguments")
        
        #get all key and check uniqueness
        keys = [key.key for arg in self.arguments for key in arg.key]
            
        if len(keys) != len(set(keys)):
            duplicate = set([key for key in keys if keys.count(key) > 1])
            raise ValueError(f"Duplicate keys found in keys, value of key is: {duplicate}")
        
    def help_info(self) -> str:
        info = f"\nModule: {self.module_name.upper()}\n"
        info += "\n".join([f"{arg.help_info}\n" for arg in self.arguments])
        return info