import enum
import typing
from abc import ABC, abstractmethod

from common.CLI.abstract_model import AbstractModel

from .keymodel import KeyModel, KeyModelTypes

class OptionAbstract(AbstractModel, ABC):
    """
    OptionAbstract class is a class that represents a flag, argument, or option.
    
    Args:
        name (str): The name of the flag, argument, or option.
        keys (List[KeyModel]): The keys of the flag, argument, or option.
        option (str|None): The displayed in [option] in the help message. If None, it will be the same as the name.
        description (str): The description of the flag, argument, or option.
        error_message (str|None): The error message of the flag, argument, or option.
    """
    keys: typing.List[KeyModel] = list()
    _value: typing.Optional[str] = None
    error_message: typing.Optional[str] = None
    option: typing.Optional[str] = None
    _require_argument: bool = True
    required: bool = False
    
    @property
    def value(self) -> typing.Optional[str]:
        return self._value
    
    @value.setter
    def value(self, value: typing.Optional[str]) -> None:
        self._value = value
        self._validate_value()
        
    @property
    def require_argument(self) -> bool:
        return self._require_argument
    
    @require_argument.setter
    def require_argument(self, require_argument: bool) -> None:
        if require_argument is not None:
            self._require_argument = require_argument
            
    @abstractmethod
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    def _validate(self) -> None:
        """
        _validate validates the flag, argument, or option.
        """
        super()._validate()
        self._validate_key()
        self._validate_value()
    
    @abstractmethod
    def _validate_value(self) -> None:
        pass
    
    def _validate_key(self) -> None:
        """
        _validate_key validates the keys of the flag, argument, or option.
        
        Raises:
            ValueError: If the flag, argument, or option has no key.
        """
        list_of_keys = [key.key for key in self.keys]
        if len(list_of_keys) == set(list_of_keys):
            raise ValueError(f"Option {self.name} has duplicate keys: \n{list_of_keys}")
        for key in self.keys:
            key._validate_key()
            
    def _validate_key_existence(self) -> None:
        """
        _validate_key validates the key of the flag.
        
        Raises:
            ValueError: If the flag has no key.
        """
        if len(self.keys) == 0:
            raise ValueError(f"Option {self.name} has no key.")
        
    def set_value(self, value) -> None:
        self._value = value
        
    def append_key(self, key: KeyModel) -> None:
        """
        append_key appends a key to the flag, argument, or option.
        
        Args:
            key (KeyModel): The key to append to the flag, argument, or option.
        """
        if key not in self.keys:
            self.keys.append(key)

    def get_help(self) -> str:
        """
        get_help gets the help message for the flag, argument, or option.
        
        Returns:
            str: The help message for the flag, argument, or option.
        """
        return f"{self.name} - {self.description}"
    
    
    def is_set(self) -> bool:
        """
        is_set checks if the flag, argument, or option is set.
        
        Returns:
            bool: True if the flag, argument, or option is set, False otherwise.
        """
        return self._value is not None
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    def get_option_str(self) -> typing.Optional[str]:
        """
        get_option gets the option of the flag, argument, or option.
        
        Returns:
            typing.Optional[str]: The option of the flag, argument, or option.
        """
        option = self.name
        if self.option:
            option =  self.option
    
        
        bracket = "[]"
        if self.require_argument:
            bracket = "<>"
        return f"{bracket[0]}{option}{bracket[1]}"
    
    def get_keys(self) -> typing.List[str]:
        """
        get_keys gets the keys of the flag, argument, or option.
        
        Returns:
            typing.List[str]: The keys of the flag, argument, or option.
        """
        return [key.key for key in self.keys]
    
    def get_keys_str(self) -> str:
        """
        get_keys_str gets the keys of the flag, argument, or option as a string.
        
        Returns:
            str: The keys of the flag, argument, or option as a string.
        """
        styled_keys = [f"-{key.key}" if key.type == KeyModelTypes.letter else f"--{key.key}" for key in self.keys]
            
        option_str = ""
        join_str = ", "
        if self.__class__.__name__ != "Flag":
            option_str = self.get_option_str()
            
            join_str = f" {option_str}{join_str}"
            
        output =  join_str.join(styled_keys)
        
        if self.__class__.__name__ != "Flag":
            output += f" {option_str}"
        
        return output
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.__repr__tuple__()}"
    
    def __repr__tuple__(self) -> typing.Tuple[str, str]:
        return (self.get_keys_str(), self.description)
    
    def __lt__(self, other) -> bool:
        super().__lt__(other)
    
    def __len__(self) -> int:
        return len(self.get_keys_str())