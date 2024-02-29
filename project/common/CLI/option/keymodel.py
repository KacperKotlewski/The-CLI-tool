import enum
from common.models.base import BaseModel

class KeyModelTypes(enum.Enum):
    letter = enum.auto()
    phrase = enum.auto()

class KeyModel(BaseModel):
    """
    KeyModel class is a class that represents a key of a flag, argument, or option.
    
    Args:
        key (str): The key of the flag, argument, or option.
        type (OptionKeyTypes): The type of the key of the flag, argument, or option.
    """
    key: str = None
    type: KeyModelTypes = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_key()
        
    def _validate_key(self):
        """
        _validate_key validates the key of the flag, argument, or option.
        
        Raises:
            ValueError: If the key of the flag, argument, or option is not valid.
        """
        if self.type == KeyModelTypes.letter:
            if not self.key.isalpha():
                raise ValueError(f"Key {self.key} is not alphabetic")
            if len(self.key) != 1:
                raise ValueError(f"Key {self.key} is not a single letter")
            
        elif self.type == KeyModelTypes.phrase:
            if not isinstance(self.key, str):
                raise ValueError(f"Key {self.key} is not a string")
            
        else:
            raise ValueError(f"Key {self.key} has invalid type: {self.type}")
