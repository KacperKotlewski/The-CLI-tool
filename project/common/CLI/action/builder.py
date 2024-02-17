import typing
from common.models.base import BaseModel

from .action import Action


class ActionBuilder(BaseModel):
    action: Action = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        if not self.action:
            self.action = Action()
        
    def set_name(self, name: str) -> 'ActionBuilder':
        self.action.name = name
        return self
    
    def set_function(self, function: typing.Callable) -> 'ActionBuilder':
        self.action.function = function
        return self
    
    def set_condition(self, condition: typing.Callable) -> 'ActionBuilder':
        self.action.condition = condition
        return self
        
    def build(self) -> Action:
        return self.action
    
    