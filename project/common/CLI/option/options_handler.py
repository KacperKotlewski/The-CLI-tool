from .keymodel import KeyModelTypes
from .option_abstract import OptionAbstract, OptionType
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
        
        type = KeyModelTypes.phrase
        if len(key) == 2:
            type = KeyModelTypes.letter
            
        for option in self.options:
            for k in [km.key for km in option.keys if km.type == type]:
                if k == key:
                    return option
        return None
    
    def handle_args(self, args: typing.List[str]) -> None:
        """
        handle_args handles the arguments of the flags, arguments, and options.
        
        Args:
            args (typing.List[str]): The arguments of the flags, arguments, and options.
        """
        index = 0
        queue_of_arguments = [option for option in self.options if option._type == OptionType.argument]
        while index < len(args):
            arg = args[index]
            if arg.startswith("-"):
                option = self.get_option_by_key(arg)
                if option:
                    if option._type == OptionType.flag:
                        option.set_value()
                    else:
                        index += 1
                        option.set_value(args[index])
            else:
                option = queue_of_arguments.pop(0)
                option.set_value(arg)
            index += 1
        