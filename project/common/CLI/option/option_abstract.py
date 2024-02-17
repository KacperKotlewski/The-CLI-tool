import enum
import typing
from abc import ABC, abstractmethod

from common.models.base import BaseModel

from .keymodel import KeyModel

class OptionAbstract(BaseModel, ABC):
    """
    OptionAbstract class is a class that represents a flag, argument, or option.
    
    Args:
        name (str): The name of the flag, argument, or option.
        keys (typing.List[KeyModel]): The keys of the flag, argument, or option.
        description (str): The description of the flag, argument, or option.
    """
    name: str = None
    keys: typing.List[KeyModel] = list()
    description: str = None
    _value: typing.Optional[str] = None
    
    @property
    def value(self) -> typing.Optional[str]:
        return self._value
    
    @value.setter
    def value(self, value: typing.Optional[str]) -> None:
        self._value = value
        self._validate_value()
            
    @abstractmethod
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    def _validate(self) -> None:
        """
        _validate validates the flag, argument, or option.
        """
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
            raise ValueError(f"Flag {self.name} has no key")
        
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