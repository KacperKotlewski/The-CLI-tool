import typing
from common.CLI.abstract_model import AbstractModel

# action is made from a function and a conditionfrom common.CLI.abstract_model import AbstractModel

class Action(AbstractModel):
    """
    """
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
        
    
    def __len__(self) -> int:
        return super().__len__()