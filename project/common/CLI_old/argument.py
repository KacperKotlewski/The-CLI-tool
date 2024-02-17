
from ._argument_base import ArgumentLikeBase
import enum

class ArgumentTypes(enum.Enum):
    required = 1
    optional = 2
    variadic = 3

class Argument(ArgumentLikeBase):
    type:ArgumentTypes = None
    
    def __init__(self, **data) -> None:
        super().__init__(**data)