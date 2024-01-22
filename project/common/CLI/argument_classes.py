import enum

from common.models.base import BaseModel
import typing

class ArgumentComplexity(enum.Enum):
    value_only = enum.auto()
    key_only = enum.auto()
    key_and_value = enum.auto()
    
class ArgumentKeyTypes(enum.Enum):
    letter = enum.auto()
    phrase = enum.auto()
    
class ArgumentValueTypes(enum.Enum):
    single = enum.auto()
    multiple = enum.auto()
    
class KeyModel(BaseModel):
    key: typing.Optional[str] = None
    type: ArgumentKeyTypes = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_key()
        
    def _validate_key(self):
        if self.type == ArgumentKeyTypes.letter:
            if not self.key.isalpha():
                raise ValueError(f"Key {self.key} is not alphabetic")
            if len(self.key) != 1:
                raise ValueError(f"Key {self.key} is not a single letter")
            
        elif self.type == ArgumentKeyTypes.phrase:
            if not isinstance(self.key, str):
                raise ValueError(f"Key {self.key} is not a string")
            
        else:
            raise ValueError(f"Key {self.key} has invalid type: {self.type}")
            
    
class ValueModel(BaseModel):
    value: typing.Optional[str] = None
    type: ArgumentValueTypes = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_value()
        
    def _validate_value(self):
        if self.type == ArgumentValueTypes.single:
            if not isinstance(self.value, str):
                raise ValueError(f"Value {self.value} is not a string")
            
        elif self.type == ArgumentValueTypes.multiple:
            if not isinstance(self.value, list) or not all(isinstance(v, str) for v in self.value):
                raise ValueError(f"Value {self.value} is not a list of strings")
            
        else:
            raise ValueError(f"Value {self.value} has invalid type: {self.type}")
    
class Argument(BaseModel):
    name: str = None
    help_info: str = None
    complexity: ArgumentComplexity = None
    key: typing.List[KeyModel] = list()
    value: typing.Optional[typing.Union[ValueModel, typing.List[ValueModel]]] = None
    action: typing.Optional[typing.Callable] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_complexity()
        
    def _validate_complexity(self):
        exist = {
            "key": len(self.key) != 0,
            "value": self.value is not None,
        }
        
        not_exist= { k: not v for k, v in exist.items() }
        
        if self.complexity == ArgumentComplexity.key_only:
            # if key not exist, raise error
            if not_exist["key"]:
                raise ValueError(f"Argument {self.name} has complexity key_only but no key")
            # if value exist, raise error
            if exist["value"]:
                raise ValueError(f"Argument {self.name} has complexity key_only but has value")
            
        elif self.complexity == ArgumentComplexity.key_and_value:
            # if key not exist, raise error
            if not_exist["key"]:
                raise ValueError(f"Argument {self.name} has complexity key_and_value but no key")
            # if value not exist, raise error
            if not_exist["value"]:
                raise ValueError(f"Argument {self.name} has complexity key_and_value but no value")
            
        elif self.complexity == ArgumentComplexity.value_only:
            # if key exist, raise error
            if exist["key"]:
                raise ValueError(f"Argument {self.name} has complexity value but has key")
            # if value not exist, raise error
            if not_exist["value"]:
                raise ValueError(f"Argument {self.name} has complexity value but no value")
            
        else:
            raise ValueError(f"Argument {self.name} has invalid complexity: {self.complexity}")