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
    keys: typing.List[KeyModel] = list()
    description: str = None
    value: typing.Optional[str] = None
    
    def __init__(self) -> None:
        pass    
        
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
        return Argument(
            name=self.name,
            keys=deepcopy(self.keys),
            description=self.description,
            value=self.value
        )
    
    def build_option(self) -> Option:
        """
        build_option builds an option.
        
        Returns:
            Option: The option object.
        """
        return Option(
            name=self.name,
            keys=deepcopy(self.keys),
            description=self.description,
            value=self.value
        )
