from .option_abstract import OptionAbstract
from .flag import Flag
from .argument import Argument
from .option import Option
from .option_builder import OptionBuilder

import typing

class OptionFactory:
    """
    OptionFactory class is a class that creates a flag, argument, or option.
    """
        
    # function that makes a universal builder for all functions later
    @classmethod
    def _create_builder(self, name: str, keys: typing.List[str], description: str) -> OptionBuilder:
        """
        __create_builder creates a builder for a abstract_instance, flag, argument, or option.

        Args:
            name (str): The name of the flag, argument, or option.
            keys (typing.List[str]): The keys of the flag, argument, or option.
            description (str): The description of the flag, argument, or option.

        Returns:
            OptionBuilder: The OptionBuilder object.
        """
        builder = OptionBuilder()
        builder.set_name(name)
        for key in keys:
            builder.add_key(key)
        builder.set_description(description)
        return builder
    
    @classmethod
    def flag(self, name: str, keys: typing.List[str], description: str) -> Flag:
        """
        create_flag creates a flag.
        
        Args:
            name (str): The name of the flag.
            keys (typing.List[str]): The keys of the flag.
            description (str): The description of the flag.
            
        Returns:
            Flag: The flag object.
        """
        builder = self._create_builder(name, keys, description)
        flag = builder.build_flag()
        return flag
    
    @classmethod
    def argument(self, name: str, keys: typing.List[str], description: str, default_value: typing.Optional[str] = None) -> Argument:
        """
        create_argument creates an argument.
        
        Args:
            name (str): The name of the argument.
            keys (typing.List[str]): The keys of the argument.
            description (str): The description of the argument.
            default_value (typing.Optional[str]): The default value of the argument.
            
        Returns:
            Argument: The argument object.
        """
        builder = self._create_builder(name, keys, description)
        builder.set_value(default_value)
        argument = builder.build_argument()
        return argument
    
    @classmethod
    def option(self, name: str, keys: typing.List[str], description: str, default_value: typing.Optional[str] = None) -> Option:
        """
        create_option creates an option.
        
        Args:
            name (str): The name of the option.
            keys (typing.List[str]): The keys of the option.
            description (str): The description of the option.
            default_value (typing.Optional[str]): The default value of the option.
            
        Returns:
            Option: The option object.
        """
        builder = self._create_builder(name, keys, description)
        builder.set_value(default_value)
        option = builder.build_option()
        return option
    