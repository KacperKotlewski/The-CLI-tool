from copy import deepcopy
import typing

from .option_abstract import OptionAbstract
from .keymodel import KeyModelTypes, KeyModel

class OptionBuilder:
    """
    OptionBuilder class is a class that builds a flag, argument, or option.
    """
    def __init__(self) -> None:
        self.option = OptionAbstract()
        
    def set_name(self, name: str) -> 'OptionBuilder':
        """
        set_name sets the name of the option.
        
        Args:
            name (str): The name of the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.option.name = name
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
        
        self.option.append_key(KeyModel(key=key, type=type))
        return self
    
    def set_description(self, description: str) -> 'OptionBuilder':
        """
        set_description sets the description of the option.
        
        Args:
            description (str): The description of the option.

        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.option.description = description
        return self
    
    def set_value(self, value: typing.Optional[str]) -> 'OptionBuilder':
        """
        set_value sets the value of the option.
        
        Args:
            value (typing.Optional[str]): The value of the option.
            
        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        self.option.value = value
        return self
    
    def build(self) -> OptionAbstract:
        return deepcopy(self.option)
