from .argument import Argument
from ._argument_base import ArgumentLikeBase
from common.models.base import BaseModel
import typing
import enum


class OptionValueTypes(enum.Enum):
    single = enum.auto()
    multiple = enum.auto()

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
    
    

class WithArgumentBase(ArgumentLikeBase):
    arguments: typing.List[Argument] = list()
    value: typing.Optional[typing.Union[ValueModel, typing.List[ValueModel]]] = None
    action: typing.Optional[typing.Callable] = None
    
    def __init__(self, **data):
        super().__init__(**data)
    
    def run_action(self, cli_module, *args, **kwargs) -> None:
        if self.action is None:
            raise ValueError(f"Element {self.name} has no action")
        
        self.action(cli_module, *args, **kwargs)
        
    def is_action_set(self) -> bool:
        return self.action is not None
    
    def __call__(self, *args: typing.Any, **kwds: typing.Any) -> typing.Any:
        if self.is_action_set():
            self.run_action(*args, **kwds)
            
    def get_stylized_details(self, strlen: int) -> str:
        return f'{self.name:<{strlen}s}'
    
    def get_details_len(self) -> int:
        return len(self.name)
    
    def run_argument(self, argument_name: str, args) -> None:
        pass