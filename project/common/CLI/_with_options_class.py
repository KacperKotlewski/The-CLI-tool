import enum
from copy import deepcopy

from common.models.base import BaseModel
import typing
from . import options as o

class BaseWithOptions(BaseModel):
    options: typing.List[o.Option] = list()
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_options()
        
    def _validate_options(self) -> None:
        if not isinstance(self.options, list):
            raise ValueError(f"Options {self.options} is not a list")
        
        if not all(isinstance(arg, o.Option) for arg in self.options):
            raise ValueError(f"Options {self.options} is not a list of options")
        
        #get all key and check uniqueness
        keys = [key.key for arg in self.options for key in arg.key]
            
        if len(keys) != len(set(keys)):
            duplicate = set([key for key in keys if keys.count(key) > 1])
            raise ValueError(f"Duplicate keys found in keys, value of key is: {duplicate}")
        
    def get_details(self) -> str:
        info = ""
        if len(self.options) > 0:
            info += f"\nOptions:\n"
            strlen = max([opt.get_details_len() for opt in self.options])
            
            info += "\n".join([f'  {opt.get_stylized_details(strlen)}' for opt in self.options]) +"\n"
            
        return info
    
    def get_option_help_info(self, option_name: str) -> str:
        option = self.get_option(option_name)
        return option.get_details
    
    def get_option(self, option_name: str) -> o.Option:
        for option in self.options:
            if option.name == option_name:
                return option
        raise ValueError(f"option {option_name} not found")
    
    def get_option_by_key_letter(self, key_letter: str) -> o.Option:
        for option in self.options:
            for arg_key in option.key:
                if arg_key.type == o.OptionKeyTypes.letter and arg_key.key == key_letter:
                    return option
        raise ValueError(f"Option with key \"-{key_letter}\" not found")
    
    def get_option_by_key_phrase(self, key_phrase: str) -> o.Option:
        for option in self.options:
            for arg_key in option.key:
                if arg_key.type == o.OptionKeyTypes.phrase and arg_key.key == key_phrase:
                    return option
        raise ValueError(f"option with key \"--{key_phrase}\" not found")
    
    def get_option_by_key(self, key: str) -> o.Option:
        if key.startswith("--"):
            return self.get_option_by_key_phrase(key.strip("-"))
        
        elif key.startswith("-"):
            return self.get_option_by_key_letter(key.strip("-"))
        
        else:
            raise ValueError(f"Invalid key: {key}")
        
    def run_option(self, option_name: str, args) -> None:
        option = self.get_option_by_key(option_name)
        
        if option is None:
            raise ValueError(f"option {option_name} not found")
        
        if option.complexity != o.OptionComplexity.key_only:
            pass
        
        if option.is_action_set():
            option(self, args)
            