

from abc import ABC, abstractmethod
import typing
from common.CLI.abstract_model import AbstractModel


class Interface(AbstractModel, ABC):    
    """
    Interface is the interface class.
    
    Args:
        name (str): The name of the interface.
        description (str): The description of the interface.
    """
    
    def __init__(self, **data) -> None:
        return super().__init__(**data)
    
    def _validate(self) -> None:
        """
        _validate validates the interface.
        """
        return super()._validate()
    
    def __len__(self) -> int:
        return super().__len__()
    
    @abstractmethod
    def prompt(self, message: str, *args, **kwargs) -> str:
        """
        prompt prompts the user for input.
        
        Args:
            message (str): The message to prompt the user.
        """
        pass
    
    @abstractmethod
    def confirm(self, message: str, *args, **kwargs) -> bool:
        """
        confirm confirms the user for input.
        
        Args:
            message (str): The message to confirm the user.
        """
        pass
    
    @abstractmethod
    def choose(self, message: str, choices: typing.List[str], *args, **kwargs) -> int:
        """
        choose prompts the user for input.
        
        Args:
            message (str): The message to prompt the user.
            choices (List[str]): The choices to choose from.
        """
        pass
    
    @abstractmethod
    def message(self, message: str, *args, **kwargs) -> None:
        """
        message outputs a message.
        
        Args:
            message (str): The message to output.
        """
        pass