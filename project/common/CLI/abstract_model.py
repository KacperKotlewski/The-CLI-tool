from abc import ABC, abstractmethod

from pydantic import Field
from common.logger_model import LoggerModel
from common.utils.string_manipulation import fit_in_space, to_words, spaced_fit

class AbstractModel(LoggerModel, ABC):
    """
    AbstractModel class is a class that represents a model.
    
    Args:
        name (str): The name of the model.
        description (str): The description of the model.
    """
    name: str = None
    description: str = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    @abstractmethod
    def _validate(self) -> None:
        """
        _validate validates the model.
        """
        self._validate_name()
        self._validate_description()
        
    def _validate_name(self) -> None:
        """
        _validate_name validates the name of the model.
        
        Raises:
            ValueError: If the name of the model is not set.
        """
        
        if not self.name:
            raise ValueError("Model name not set.")
        
    def _validate_description(self) -> None:
        """
        _validate_description validates the description of the model.
        
        Raises:
            ValueError: If the description of the model is not set.
        """
        
        if not self.description:
            raise ValueError("Model description not set.")
        
    @abstractmethod
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
    
    @abstractmethod
    def __repr__tuple__(self) -> str:
        return (self.name, self.description)
    
    @abstractmethod
    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"
    
    @abstractmethod
    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractModel):
            raise ValueError("Can only compare with AbstractModel.")
        return len(self) > len(other)
    
    @abstractmethod
    def __len__(self) -> int:
        return len(self.__repr__()[0])
    
    def spaced_description(self, taken:int, total:int) -> str:
        l = total - taken
        AbstractModel.log_strict(l, taken, total)
        
        return spaced_fit(self.description, taken, total)
    
    def stylized_representation(self, total_space:int=None, space_before:int=None, space_after:int=None, first_str_length:int=None, second_str_length:int=None) -> str:
        """
        stylized_presentation stylizes the presentation of the model.
        
        Args:
            total_space (int): The total space. Default is None.
            space_before (int): The space before the model. Default is None.
            space_after (int): The space after the model. Default is None.
            first_str_length (int): The length of the first string. Default is None.
            second_str_length (int): The length of the second string. Default is None.
        """        
        return fit_in_space(
            list(self.__repr__tuple__()),
            total_space=total_space, 
            space_before=space_before, 
            space_between=space_after, 
            str_length=[first_str_length, second_str_length]
        )