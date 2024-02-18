from .keymodel import KeyModelTypes

from .option_abstract import OptionAbstract
from .argument import Argument
from .flag import Flag
from .option import Option

from common.models.base import BaseModel

import typing

class OptionHandler(BaseModel):
    """
    OptionsHandler class is a class that handles flags, arguments, and options.
    """
    options: typing.List[OptionAbstract] = list()
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate(self) -> None:
        """
        _validate validates the flags, arguments, and options.
        """
        self._validate_options()
        
    def _validate_options(self) -> None:
        """
        _validate_options validates the flags, arguments, and options.
        """
        # check for duplicate names
        list_of_names = [option.name for option in self.options]
        if len(list_of_names) != len(set(list_of_names)):
            raise ValueError(f"OptionsHandler has duplicate names: \n{list_of_names}")
        
        # check for duplicate keys
        list_of_keys = [key.key for option in self.options for key in option.keys]
        if len(list_of_keys) != len(set(list_of_keys)):
            raise ValueError(f"OptionsHandler has duplicate keys: \n{list_of_keys}")
        
        for option in self.options:
            option._validate()

    def add_option(self, option: OptionAbstract) -> None:
        """
        add_option adds a flag, argument, or option to the options handler.
        
        Args:
            option (OptionAbstract): The flag, argument, or option to add to the options handler.
        """
        if option not in self.options:
            self.options.append(option)
            self._validate_options()
            
    def insert_option(self, index: int, option: OptionAbstract) -> None:
        """
        insert_option inserts a flag, argument, or option into the options handler at the given index.
        
        Args:
            index (int): The index to insert the flag, argument, or option into the options handler.
            option (OptionAbstract): The flag, argument, or option to insert into the options handler.
        """
        if option not in self.options:
            self.options.insert(index, option)
            self._validate_options()
            
    def remove_option(self, option: OptionAbstract) -> None:
        """
        remove_option removes a flag, argument, or option from the options handler.
        
        Args:
            option (OptionAbstract): The flag, argument, or option to remove from the options handler.
        """
        if option in self.options:
            self.options.remove(option)
            self._validate_options()
            
    def get_option_by_name(self, name: str) -> OptionAbstract:
        """
        get_option_by_name gets a flag, argument, or option from the options handler by name.
        
        Args:
            name (str): The name of the flag, argument, or option to get from the options handler.
            
        Returns:
            OptionAbstract: The flag, argument, or option from the options handler by name.
        """
        for option in self.options:
            if option.name == name:
                return option
        return None
    
    def get_option_by_key(self, key: str) -> OptionAbstract:
        """
        get_option_by_key gets a flag, argument, or option from the options handler by key.
        
        Args:
            key (str): The key of the flag, argument, or option to get from the options handler. Example: '-k', '--key'.
            
        Returns:
            OptionAbstract: The flag, argument, or option from the options handler by key.
        """
        if not key.startswith("-"):
            raise ValueError(f"Key {key} is not a valid key, all keys must start with '-' or '--'")
        
        key = key.strip("-")
        
        type = KeyModelTypes.phrase
        if len(key) == 1:
            type = KeyModelTypes.letter
            
        for option in self.options:
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
    
    def handle_args(self, *args: str) -> int:
        """
        handle_args handles the arguments of the flags, arguments, and options.
        
        Args:
            args (typing.List[str]): The arguments of the flags, arguments, and options.
        """
        count_of_executed_options = 0
        index = 0
        queue_of_arguments = [option for option in self.options if isinstance(option, Argument)]
        
        while index < len(args):
            arg = args[index]
                        
            if arg.startswith("-"):
                option = self.get_option_by_key(arg)
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
        
    def __add__(self, other: typing.Union['OptionHandler', OptionAbstract]) -> 'OptionHandler':
        """
        __add__ adds two options handlers together or an option handler and an option.
        
        Args:
            other (typing.Union[OptionHandler, OptionAbstract]): The other option handler or option to add.
            
        Returns:
            OptionHandler: The option handler with the other option handler or option added.
        """
        if isinstance(other, OptionHandler):
            for option in other.options:
                try:
                    self.add_option(option)
                except ValueError as e:
                    pass # ignore duplicate options
        elif isinstance(other, OptionAbstract):
            self.add_option(other)
        return self
    
    def __str__(self) -> str:
        """
        __str__ gets the string representation of the options handler.
        
        Returns:
            str: The string representation of the options handler.
        """
        return f"OptionsHandler: \n\t" + "\t\n".join([str(option) for option in self.options])
    
    
    def __len__(self) -> int:
        return len(self.options)