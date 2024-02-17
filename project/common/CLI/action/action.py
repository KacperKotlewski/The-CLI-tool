import typing
from common.models.base import BaseModel

# action is made from a function and a condition
class Action(BaseModel):
    name: str = None
    function: typing.Callable = None
    condition: typing.Callable = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate()
        
    def _validate(self) -> None:
        self._validate_function()
        self._validate_condition()
        
    def _validate_function(self) -> None:
        if not self.function:
            raise ValueError(f"Action has no function: {self.function}")
        
    def _validate_condition(self) -> None:
        if not self.condition:
            raise ValueError(f"Action has no condition: {self.condition}")
        
    def execute(self, *args, **kwargs) -> typing.Optional[typing.Tuple[bool, typing.Any]]:
        if self.condition(*args, **kwargs):
            return True, self.function(*args, **kwargs)
