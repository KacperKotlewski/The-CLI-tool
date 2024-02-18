from typing import List

from pydantic import Field
from .keymodel import KeyModelTypes

from .option_abstract import OptionAbstract
from .argument import Argument
from .flag import Flag
from .option import Option

from common.models.base import BaseModel
from common.CLI.abstract_handler import AbstractHandler

import typing

class OptionHandler(AbstractHandler, BaseModel):
    """
    OptionsHandler class is a class that handles flags, arguments, and options.
    
    Args:
        items (List[OptionAbstract]): The flags, arguments, and options of the handler.
    """
    items: typing.List[OptionAbstract] = list()
    items_instance: typing.Type = Field(default=OptionAbstract)
        
    def _validate_duplicates(self) -> None:
        super()._validate_duplicates()
        self._validate_keys_duplicates()
        
    def _validate_keys_duplicates(self) -> None:
        """
        _validate_keys_duplicates checks for duplicate keys.
        
        Raises:
            ValueError: If there are duplicate keys.
        """
        list_of_keys = [key.key for option in self.items for key in option.keys]
        if len(list_of_keys) != len(set(list_of_keys)):
            raise ValueError(f"OptionsHandler has duplicate keys: \n{list_of_keys}")
    
    def get_by_key(self, key: str) -> OptionAbstract:
        """
        get_option_by_key gets a flag, argument, or option from the options handler by key.
        
        Args:
            key (str): The key of the flag, argument, or option to get from the options handler. Example: '-k', '--key'.
            
        Returns:
            OptionAbstract: The flag, argument, or option from the options handler by key.
        """
        if not key.startswith("-"):
            raise ValueError(f"Key {key} is not a valid key, all keys must start with '-' or '--'")
        
        
        type = KeyModelTypes.phrase
        if len(key) == 2:
            type = KeyModelTypes.letter
            
        key = key.strip("-")
        for option in self.items:
            for k in [km.key for km in option.keys if km.type == type]:
                if k == key:
                    return option
        return None
    
    def get_help(self) -> str:
        """
        get_help gets the help message for the flags, arguments, and options.
        
        Returns:
            str: The help message for the flags, arguments, and options.
        """
        help_str = ""
        for option in self.options:
            help_str += option.get_help() + "\n"
        return help_str
    
    def execute(self, *args: str) -> int:
        """
        handle_args handles the arguments of the flags, arguments, and options.
        
        Args:
            args (typing.List[str]): The arguments of the flags, arguments, and options.
        """
        count_of_executed_options = 0
        index = 0
        queue_of_arguments = [option for option in self.items if isinstance(option, Argument)]
        
        while index < len(args):
            arg = args[index]
                        
            if arg.startswith("-"):
                option = self.get_by_key(arg)
                if option:
                    if isinstance(option, Flag):
                        option.set_value()
                        count_of_executed_options += 1
                    elif isinstance(option, Option):
                        #handle option with argument, catch the next argument, if it is not a flag or not empty set the value of the option to the argument, else treat it as a flag
                        try:
                            next_arg = args[index+1]
                            if next_arg.startswith("-"):
                                raise IndexError("Next argument is a flag.")
                            option.set_value(next_arg)
                            index += 1
                            
                        except IndexError as e: # threat as flag
                            option.set_value()
                            
                        count_of_executed_options += 1
                    else:
                        raise ValueError(f"Option {option.name} is not a valid option. \n\t{option}")
                            
            elif len(queue_of_arguments) > 0:
                option = queue_of_arguments.pop(0)
                option.set_value(arg)
                count_of_executed_options += 1
            else:
                raise ValueError(f"Option {option.name} is not a valid option. \n\t{option}")
            index += 1
            
        return count_of_executed_options
    
    def __str__(self) -> str:
        return f"OptionsHandler: \n\t" + "\t\n".join([str(option) for option in self.items])
    
    
    
    
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate(self) -> None:
        super()._validate()
        
    def _validate_items(self) -> None:
        super()._validate_items()
        
    def check_item_duplicates(self, item: OptionAbstract) -> bool:
        return super().check_item_duplicates(item)
        
    def check_item_instance(self, item: OptionAbstract) -> bool:
        return super().check_item_instance(item)
        
    def verify_item(self, item: OptionAbstract) -> bool:
        return super().verify_item(item)
        
    def add(self, option: OptionAbstract) -> None:
        super().add(option)
            
    def extend(self, items: List[OptionAbstract]) -> None:
        return super().extend(items)
    
    def insert(self, index: int, option: OptionAbstract) -> None:
        super().insert(index, option)
            
    def remove(self, option: OptionAbstract) -> None:
        super().remove(option)
            
    def get(self, name: str) -> OptionAbstract:
        return super().get(name)    
    
    def __add__(self, other: typing.Union['OptionHandler', OptionAbstract, list]) -> 'OptionHandler':
        return super().__add__(other)
    
    def __len__(self) -> int:
        return super().__len__()
    
    def __iter__(self) -> typing.Iterator[OptionAbstract]:
        return super().__iter__()
    
    def __lt__(self, other: 'OptionHandler') -> bool:
        return super().__lt__(other)
    