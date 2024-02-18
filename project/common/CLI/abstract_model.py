from abc import ABC, abstractmethod

from pydantic import Field
from common.logger_model import LoggerModel
from common.debug import log_section

def cut_strings_to_words(string:str, taken:int, total:int):
    words = string.split()
    lines = []
    current_line = ' ' * taken
    log_section("cut_strings_to_words", word)
    for word in words:
        log_section("cut_strings_to_words", len(current_line), len(word) + 1, total, current_line, word)
        
        # split the word if it's too long
        while len(word) > total:
            lines.append(current_line + word[:total-2])
            word = word[total-2:]
            current_line = ' ' * taken
        
        # add the word to the current line if it fits  
        if len(current_line) + len(word) + 1 <= total:
            current_line += ' ' + word
            
        # start a new line if it doesn't fit
        else:
            lines.append(current_line)
            current_line = ' ' * taken + word
                
    lines.append(current_line)
    return '\n'.join(lines)


def terminal_width() -> int:
    try:
        try:
            from blessed import Terminal
            term = Terminal()
            width = term.width
        except ImportError:
            import shutil
            width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
        
    return width

class RepresentationSettings:
    TOTAL_SPACE: int = None
    SPACE_BEFORE: int = 0
    SPACE_AFTER: int = 1
    
    @staticmethod
    def set_total_space(space:int) -> None:
        RepresentationSettings.TOTAL_SPACE = space
    
    @staticmethod
    def set_space_before(space:int) -> None:
        RepresentationSettings.SPACE_BEFORE = space
    
    @staticmethod
    def set_space_after(space:int) -> None:
        RepresentationSettings.SPACE_AFTER = space
        
    @staticmethod
    def reset_total_space() -> None:
        RepresentationSettings.TOTAL_SPACE = None
        
    @staticmethod
    def reset_space_before() -> None:
        RepresentationSettings.SPACE_BEFORE = 0
        
    @staticmethod
    def reset_space_after() -> None:
        RepresentationSettings.SPACE_AFTER = 1
        
    @staticmethod
    def total_space() -> int:
        if RepresentationSettings.TOTAL_SPACE is None:
            return terminal_width()
        return RepresentationSettings.TOTAL_SPACE
    
    @staticmethod
    def space_before() -> int:
        return RepresentationSettings.SPACE_BEFORE
    
    @staticmethod
    def space_after() -> int:
        return RepresentationSettings.SPACE_AFTER

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
        if l < 10:
            raise ValueError("Total length is less than taken length. Need at least 10 characters.")
        
        if len(self.description) < l:
            return ' ' * taken + self.description
        
        return cut_strings_to_words(self.description, taken, total)
    
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
        
        repr_str = self.__repr__tuple__()
        
        if total_space is None:
            total_space = RepresentationSettings.total_space()
            
        if space_before is None:
            space_before = RepresentationSettings.space_before()
            
        if space_after is None:
            space_after = RepresentationSettings.space_after()
        
        if first_str_length is None:
            first_str_length = len(repr_str[0])
            
        space_before_second = first_str_length + space_before + space_after
            
        if second_str_length is None:
            second_str_length = min(len(self.description), (total_space - space_before_second))
        
        return (
            " " * space_before + 
            repr_str[0].ljust(first_str_length) + 
            " " * space_after + 
            self.spaced_description(space_before_second, total_space)[space_before_second:]
        )