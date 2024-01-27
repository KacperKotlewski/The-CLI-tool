import enum

from common.models.base import BaseModel
from ._with_help_class import BaseWithPropertyHelp
import typing

class OptionComplexity(enum.Enum):
    value_only = enum.auto()
    key_only = enum.auto()
    key_and_value = enum.auto()
    
class OptionKeyTypes(enum.Enum):
    letter = enum.auto()
    phrase = enum.auto()
    
class OptionValueTypes(enum.Enum):
    single = enum.auto()
    multiple = enum.auto()
    
class KeyModel(BaseModel):
    key: typing.Optional[str] = None
    type: OptionKeyTypes = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_key()
        
    def _validate_key(self):
        if self.type == OptionKeyTypes.letter:
            if not self.key.isalpha():
                raise ValueError(f"Key {self.key} is not alphabetic")
            if len(self.key) != 1:
                raise ValueError(f"Key {self.key} is not a single letter")
            
        elif self.type == OptionKeyTypes.phrase:
            if not isinstance(self.key, str):
                raise ValueError(f"Key {self.key} is not a string")
            
        else:
            raise ValueError(f"Key {self.key} has invalid type: {self.type}")
            
    
class ValueModel(BaseModel):
    value: typing.Optional[str] = None
    type: OptionValueTypes = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_value()
        
    def _validate_value(self):
        if self.type == OptionValueTypes.single:
            if not isinstance(self.value, (str, type(None))):
                raise ValueError(f"Value {self.value} is not a string")
            
        elif self.type == OptionValueTypes.multiple:
            if not isinstance(self.value, list) or not all(isinstance(v, str) for v in self.value):
                raise ValueError(f"Value {self.value} is not a list of strings")
            
        else:
            raise ValueError(f"Value {self.value} has invalid type: {self.type}")
    
class Option(BaseWithPropertyHelp):
    name: str = None
    complexity: OptionComplexity = None
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
        
        if self.complexity == OptionComplexity.key_only:
            # if key not exist, raise error
            if not_exist["key"]:
                raise ValueError(f"Option {self.name} has complexity key_only but no key")
            # if value exist, raise error
            if exist["value"]:
                raise ValueError(f"Option {self.name} has complexity key_only but has value")
            
        elif self.complexity == OptionComplexity.key_and_value:
            # if key not exist, raise error
            if not_exist["key"]:
                raise ValueError(f"Option {self.name} has complexity key_and_value but no key")
            # if value not exist, raise error
            if not_exist["value"]:
                raise ValueError(f"Option {self.name} has complexity key_and_value but no value")
            
        elif self.complexity == OptionComplexity.value_only:
            # if key exist, raise error
            if exist["key"]:
                raise ValueError(f"Option {self.name} has complexity value but has key")
            # if value not exist, raise error
            if not_exist["value"]:
                raise ValueError(f"Option {self.name} has complexity value but no value")
            
        else:
            raise ValueError(f"Option {self.name} has invalid complexity: {self.complexity}")
        
    def _get_letter_keys(self) -> typing.List[str]:
        return [key.key for key in self.key if key.type == OptionKeyTypes.letter]
    
    def _get_phrase_keys(self) -> typing.List[str]:
        return [key.key for key in self.key if key.type == OptionKeyTypes.phrase]
    
    def check_key_letter(self, key: str) -> bool:
        return key in self._get_letter_keys()
    
    def check_key_phrase(self, key: str) -> bool:
        return key in self._get_phrase_keys()
    
    def run_action(self, cli_module, *args, **kwargs) -> None:
        if self.action is None:
            raise ValueError(f"Option {self.name} has no action")
        
        self.action(cli_module, *args, **kwargs)
        
    def is_action_set(self) -> bool:
        return self.action is not None
    
    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> typing.Any:
        if self.is_action_set():
            self.run_action(*args, **kwds)