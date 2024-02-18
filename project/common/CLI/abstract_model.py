from abc import ABC, abstractmethod
from common.models.base import BaseModel
from common.debug import log_section

# def cut_strings_to_sentences(string:str, taken:int, total:int, separator:str="."):
#     sentences = string.split(separator)
#     lines = []
#     current_line = ' ' * taken
#     for sentence in sentences:
#         print(len(current_line), len(sentence) + 1, total, current_line, sentence)
#         # split the sentence if it's too long
#         while len(sentence) > total:
#             lines.append(current_line + sentence[:total-2])
#             sentence = sentence[total-2:]
#             current_line = ' ' * taken
        
#         # add the sentence to the current line if it fits  
#         if len(current_line) + len(sentence) + 1 <= total:
#             current_line += ' ' + sentence
            
#         # start a new line if it doesn't fit
#         else:
#             lines.append(current_line)
#             current_line = ' ' * taken + sentence
                
#         lines.append(current_line)
#         return '\n'.join(lines)

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

class AbstractModel(ABC, BaseModel):
    """
    AbstractModel class is a class that represents a model.
    
    Args:
        name (str): The name of the model.
        description (str): The description of the model.
    """
    name: str = None
    description: str = None
    
    @classmethod
    def log(cls, *args, **kwargs):
        log_section(cls.__name__, *args, **kwargs)
    
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
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__()} | {self.name}: {self.description}"
    
    def description_len(self) -> int:
        return len(self.description)
    
    def spaced_description(self, taken:int, total:int) -> str:
        l = total - taken
        AbstractModel.log(l, taken, total)
        if l < 10:
            raise ValueError("Total length is less than taken length. Need at least 10 characters.")
        
        if len(self.description) < l:
            return ' ' * taken + self.description
        
        return cut_strings_to_words(self.description, taken, total)