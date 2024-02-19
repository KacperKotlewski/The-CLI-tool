from copy import deepcopy
import typing

from .option_abstract import OptionAbstract
from .keymodel import KeyModelTypes, KeyModel

from .flag import Flag
from .argument import Argument
from .option import Option

class OptionBuilder:
    """
    OptionBuilder class is a class that builds a flag, argument, or option.
    """    
    name: str = None
    keys: typing.List[KeyModel] = None
    description: str = None
    value: typing.Optional[str] = None
    require_argument: typing.Optional[str] = None
    option: typing.Optional[str] = None
    required: bool = None
    
    def __init__(self) -> None:
        self.keys = list()
        
    def set_name(self, name: str) -> 'OptionBuilder':
        """
        set_name sets the name of the option.
        
        Args:
            name (str): The name of the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.name = name
        return self
    
    def add_key(self, key: str) -> 'OptionBuilder':
        """
        add_key adds a key to the option.
        
        Args:
            key (str): The key to add to the option. Example: '-k', '--key'.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        key = key.strip()
        if key.startswith("-") and len(key) == 2:
            type = KeyModelTypes.letter
        elif key.startswith("--") and key.count(' ') == 0:
            type = KeyModelTypes.phrase
        else:
            raise ValueError(f"Key {key} is not a valid key, all keys must start with '-' or '--' and have a length of 2 or more.")
        
        key = key.strip("-").strip()
        self.keys.append(KeyModel(key=key, type=type))
        return self
    
    def add_keys(self, *keys:str) -> 'OptionBuilder':
        """
        add_keys adds a list of keys to the option.
        
        Args:
            keys (typing.List[str]): The list of keys to add to the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        for key in keys:
            self.add_key(key)
        return self
    
    def set_description(self, description: str) -> 'OptionBuilder':
        """
        set_description sets the description of the option.
        
        Args:
            description (str): The description of the option.

        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.description = description
        return self
    
    def set_value(self, value: typing.Optional[str]) -> 'OptionBuilder':
        """
        set_value sets the value of the option.
        
        Args:
            value (typing.Optional[str]): The value of the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        
        return self
    
    def set_require_argument(self, require_argument: bool) -> 'OptionBuilder':
        """
        set_require_argument sets the flag that indicates that this function can act as flag or only as an option with a value/argument.
        
        Args:
            require_argument (bool): The flag that indicates that this function can act as flag or only as an option with a value/argument.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.require_argument = require_argument
        return self
    
    def set_option(self, option: str) -> 'OptionBuilder':
        """
        set_option sets the option of the option.
        
        Args:
            option (str): The option of the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.option = option
        return self
    
    def set_required(self, required: bool) -> 'OptionBuilder':
        """
        set_required sets the flag that indicates that this option is required.
        
        Args:
            required (bool): The flag that indicates that this option is required.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.required = required
        return self
    
    def build_flag(self) -> Flag:
        """
        build_Flag builds a flag.
        
        Returns:
            Flag: The flag object.
        """
        return Flag(
            name=self.name,
            keys=deepcopy(self.keys),
            description=self.description
        )
    
    def build_argument(self) -> Argument:
        """
        build_argument builds an argument.
        
        Returns:
            Argument: The argument object.
        """
        argument =  Argument(
            name=self.name,
            keys=deepcopy(self.keys),
            description=self.description,
            value=self.value
        )
        if self.required is not None:
            argument.required = self.required
        if self.require_argument is not None:
            argument.require_argument = self.require_argument
        return argument
    
    def build_option(self) -> Option:
        """
        build_option builds an option.
        
        Returns:
            Option: The option object.
        """
        option = Option(
            name=self.name,
            keys=deepcopy(self.keys),
            description=self.description,
            value=self.value
        )
        if self.required is not None:
            option.required = self.required
        if self.require_argument is not None:
            option.require_argument = self.require_argument
        if self.option is not None:
            option.option = self.option
        return option
