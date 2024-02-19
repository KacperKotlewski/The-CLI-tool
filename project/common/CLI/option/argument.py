from typing import Tuple
from .option_abstract import OptionAbstract

import typing

class Argument(OptionAbstract):
    """
    Argument class is a class that represents an argument that has a value and can have a key.
    
    Args:
        name (str): The name of the argument.
        key (typing.List[KeyModel]): The key of the argument.
        description (str): The description of the argument.
        default_value (typing.Optional[str]): The default value of the argument.
    """
    
    def __init__(self, default_value: typing.Optional[str] = None, **data) -> None:
        if default_value is not None:
            self.value = default_value
        super().__init__(**data)

    def __str__(self) -> str:
        return f"Argument: {self.name}, {self.description}, {self.value} | keys: {self.keys}"
    
    def _validate_value(self) -> None:
        pass
    
    def __repr__tuple__(self) -> Tuple[str, str]:
        _r_t = super().__repr__tuple__()
        return (self.get_option_str(), _r_t[1])
    
    def to_option(self) -> 'Option':
        """
        to_option transmutes the argument to an option.
        
        Returns:
            Option: The option object.
        """
        if len(self.keys) == 0:
            raise ValueError("Argument must have at least one key to transmute to option.")
        from .option import Option
        option = Option(name=self.name, keys=self.keys, description=self.description, value=self.value, require_argument=True, option=self.option, required=self.required, error_message=self.error_message)
        return option