from .option_abstract import OptionAbstract
import typing

from .exceptions import *

class Option(OptionAbstract):
    """
    Option class is a class that represents an option that has a key and a value.

    Args:
        name (str): The name of the option.
        key (List[KeyModel]): The key of the option.
        description (str): The description of the option.
        default_value (Optional[str]): The default value of the option.
        error_message (str|None): The error message of the option.
        require_argument (bool): The flag that indicates that this function can act as flag or only as an option with a value/argument.
    """
    
    def __init__(self, **data) -> None:
        super().__init__(**data)
        
    def _validate_key(self) -> None:
        self._validate_key_existence()
        return super()._validate_key()
    
    def _validate_value(self) -> None:
        """
        _validate_value validates the value of the option.
        
        Raises:
            ValueError: If the value of the option is not a string.
        """
        if self.require_argument and self.value is not None and not isinstance(self.value, str):
            raise OptionNotValidError(f"Option {self.name} requires a value.")

    def __str__(self) -> str:
        return f"Option: {self.name}, {self.description}, {self.value} | keys: {self.keys}"
    
    def set_value(self, value: typing.Optional[str]=None) -> None:
        if self.require_argument and value is None:
            if self.error_message:
                raise OptionNotValidError(self.error_message)
            else:
                raise OptionNotValidError(f"Option {self.name} requires a value.")
            
        elif value is None:
            self.value = True
        else:
            self.value = value
            
    def to_flag(self) -> 'Flag':
        """
        to_flag converts the option to a flag.
        
        Returns:
            Flag: The flag object.
        """
        from .flag import Flag
        flag = Flag(name=self.name, keys=self.keys, description=self.description, error_message=self.error_message)
        if self.value not in [None, False]:
            flag.set_value(True)
            
        return flag
    
    def to_argument(self) -> 'Argument':
        """
        to_argument converts the option to an argument.
        
        Returns:
            Argument: The argument object.
        """
        from .argument import Argument
        argument = Argument(name=self.name, keys=self.keys, description=self.description, default_value=self.value)
        return argument