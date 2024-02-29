import typing
from common.models.base import BaseModel

from .action import Action


class ActionBuilder(BaseModel):
    name: str = None
    function: typing.Callable = None
    condition: typing.Callable = None
        
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def set_name(self, name: str) -> 'ActionBuilder':
        self.name = name
        return self
    
    def set_function(self, function: typing.Callable) -> 'ActionBuilder':
        self.function = function
        return self
    
    def set_condition(self, condition: typing.Callable) -> 'ActionBuilder':
        self.condition = condition
        return self
        
    def build(self) -> Action:
        return Action(name=self.name, function=self.function, condition=self.condition)
    
    