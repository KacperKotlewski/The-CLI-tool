import enum
from copy import deepcopy

from common.models.base import BaseModel
import typing
from .argument_classes import Argument, ArgumentComplexity, ArgumentKeyTypes, ArgumentValueTypes, KeyModel, ValueModel


class ModuleType(enum.Enum):
    root = enum.auto()
    user_interface = enum.auto()
    other = enum.auto()

class CLImodule(BaseModel):
    arguments: typing.List[Argument] = list()
    module_name: str = None
    module_type: ModuleType = ModuleType.other
    
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
    
    def get_argument_help_info(self, argument_name: str) -> str:
        argument = self.get_argument(argument_name)
        return argument.help_info
    
    def get_argument(self, argument_name: str) -> Argument:
        for argument in self.arguments:
            if argument.name == argument_name:
                return argument
        raise ValueError(f"Argument {argument_name} not found")
    
    def get_argument_by_key_letter(self, key_letter: str) -> Argument:
        for argument in self.arguments:
            for arg_key in argument.key:
                if arg_key.type == ArgumentKeyTypes.letter and arg_key.key == key_letter:
                    return argument
        raise ValueError(f"Argument with key \"-{key_letter}\" not found")
    
    def get_argument_by_key_phrase(self, key_phrase: str) -> Argument:
        for argument in self.arguments:
            for arg_key in argument.key:
                if arg_key.type == ArgumentKeyTypes.phrase and arg_key.key == key_phrase:
                    return argument
        raise ValueError(f"Argument with key \"--{key_phrase}\" not found")
    
    def get_argument_by_key(self, key: str) -> Argument:
        if key.startswith("--"):
            return self.get_argument_by_key_phrase(key.strip("-"))
        
        elif key.startswith("-"):
            return self.get_argument_by_key_letter(key.strip("-"))
        
        else:
            raise ValueError(f"Invalid key: {key}")